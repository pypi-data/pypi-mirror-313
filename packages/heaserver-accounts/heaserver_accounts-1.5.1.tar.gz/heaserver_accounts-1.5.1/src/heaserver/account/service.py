"""
The HEA Server AWS Accounts Microservice provides ...
"""
import logging
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import aws, awsservicelib
from heaserver.service.wstl import builder_factory, action
from heaserver.service import response, client
from heaserver.service.appproperty import HEA_DB, HEA_CACHE
from heaserver.service.heaobjectsupport import new_heaobject_from_type
from heaserver.service.wstl import add_run_time_action
from heaobject.account import AWSAccount, AccountView
from heaobject.bucket import AWSBucket
from heaobject.storage import AWSStorage
from heaobject.root import Permission, DesktopObjectDict, ViewerPermissionContext
from heaobject.volume import AWSFileSystem, Volume
from heaobject.user import NONE_USER, ALL_USERS, AWS_USER
from heaobject.util import parse_bool
from heaserver.service.sources import AWS as AWS_SOURCE
from yarl import URL
from aiohttp.web import Request, Response
from botocore.exceptions import ClientError as BotoClientError
from aiohttp.client_exceptions import ClientError, ClientResponseError
from heaserver.service.activity import DesktopObjectActionLifecycle, Status
from heaserver.service.messagebroker import publish_desktop_object
from collections.abc import Sequence
from heaserver.service.db.aws import AWSPermissionContext
from .context import AWSAccountPermissionContext
from mypy_boto3_organizations.literals import IAMUserAccessToBillingType
from typing import get_args, TypeGuard
import asyncio


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)

@routes.get('/accounts/{id}')
async def get_account_id(request: web.Request) -> web.Response:
    id_ = request.match_info['id']
    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-get',
                                            description=f'Getting account {id_}',
                                            activity_cb=publish_desktop_object) as activity:
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'accountid^{id_}')
        if (cached_value:=request.app[HEA_CACHE].get(cache_key)) is not None:
            av_dict, permissions, attribute_permissions = cached_value
        else:
            try:
                aws_account, volume_id = await _get_awsaccount_by_aws_account_id(request, id_.split('^')[1])
            except IndexError:
                raise response.status_bad_request(f'Invalid account id {id_}')
            if aws_account is None:
                raise response.status_not_found()
            else:
                context: ViewerPermissionContext[AccountView] = ViewerPermissionContext(sub)
                av = AccountView()
                av.actual_object_id = aws_account.id
                av.actual_object_type_name = aws_account.type
                av.actual_object_uri = f'awsaccounts/{aws_account.id}'
                av.display_name = aws_account.display_name
                av.owner = aws_account.owner
                av.shares = aws_account.shares
                av.created = aws_account.created
                av.modified = aws_account.modified
                av.name = aws_account.name
                av.type_display_name = aws_account.type_display_name
                av.file_system_type = aws_account.file_system_type
                av.file_system_name = aws_account.file_system_name
                share = await av.get_permissions_as_share(context)
                permissions = share.permissions
                av.shares = [share]
                av_dict = av.to_dict()
                attribute_permissions = await av.get_all_attribute_permissions(context)
                activity.new_object_type_name = AccountView.get_type_name()
                activity.new_object_id = id_
                activity.new_object_uri = f'accounts/{id_}'
                activity.new_volume_id = volume_id
                request.app[HEA_CACHE][cache_key] = (av_dict, permissions, attribute_permissions)
        return await response.get(request, av_dict, permissions=permissions,
                                    attribute_permissions=attribute_permissions)

@routes.get('/accounts')
@routes.get('/accounts/')
@action(name='heaserver-accounts-account-get-actual', rel='hea-actual', path='{+actual_object_uri}')
async def get_accounts(request: web.Request) -> web.Response:
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting all accounts',
                                                activity_cb=publish_desktop_object) as activity:
        logger = logging.getLogger(__name__)
        sub = request.headers.get(SUB, NONE_USER)
        account_ids = request.query.getall('account_id', [])
        cache_key = (sub, 'allaccountids')
        if not account_ids and (cached_value:=request.app[HEA_CACHE].get(cache_key)) is not None:
            account_view_dicts: list[DesktopObjectDict] = cached_value[0]
            volume_ids: list[str] = cached_value[1]
            permissions: list[list[Permission]] = cached_value[2]
            attribute_permissions: list[dict[str, list[Permission]]] = cached_value[3]
        else:
            volume_url = await type_to_resource_url(request, Volume)
            volumes = await client.get_all_list(request.app, volume_url, Volume, headers={SUB: sub})
            activity.new_object_type_name = AccountView.get_type_name()
            activity.new_object_uri = 'accounts/'
            account_views: list[AccountView] = []
            context: ViewerPermissionContext[AccountView] = ViewerPermissionContext(sub)
            permissions = []
            attribute_permissions = []
            volume_ids = []
            for volume in volumes:
                account_id = volume.account_id
                if account_id is None or (account_ids and account_id not in account_ids):
                    continue
                av = AccountView()
                assert volume.id is not None, 'volume.id cannot be None'
                volume_ids.append(volume.id)
                av.id = account_id
                type_, id_ = account_id.split('^')
                av.actual_object_id = id_
                av.actual_object_type_name = type_
                if type_ == AWSAccount.get_type_name():
                    av.display_name = f'AWS Account {id_}'
                    av.actual_object_uri = f'awsaccounts/{id_}'
                    av.type_display_name = 'AWS Account'
                av.owner = AWS_USER
                av.name = volume.name
                av.file_system_type = volume.file_system_type
                av.file_system_name = volume.file_system_name
                av.source = AWS_SOURCE
                av.source_detail = AWS_SOURCE
                share, attr_perms = await asyncio.gather(av.get_permissions_as_share(context),
                                                         av.get_all_attribute_permissions(context))
                av.shares = [share]
                permissions.append(share.permissions)
                attribute_permissions.append(attr_perms)
                account_views.append(av)
            account_view_dicts = [a.to_dict() for a in account_views]
            if not account_ids:
                request.app[HEA_CACHE][cache_key] = (account_view_dicts, volume_ids, permissions, attribute_permissions)
            for account_view_dict, perms, attr_perms in zip(account_view_dicts, permissions, attribute_permissions):
                request.app[HEA_CACHE][(sub, f'accountid^{account_view_dict["id"]}')] = (account_view_dict, perms, attr_perms)
        return await response.get_all(request, account_view_dicts,
                                    permissions=permissions,
                                    attribute_permissions=attribute_permissions)

@routes.options('/awsaccounts/{id}')
async def get_awsaccount_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await response.get_options(request, ['GET', 'HEAD', 'OPTIONS', 'PUT', 'DELETE'])


@routes.get('/awsaccounts/{id}')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu', path='awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-trash', rel='hea-trash hea-context-menu', path='volumes/{volume_id}/awss3trash')
@action('heaserver-accounts-awsaccount-get-self', rel='self hea-account', path='awsaccounts/{id}')
@action(name='heaserver-accounts-awsaccount-get-volume', rel='hea-volume', path='volumes/{volume_id}')
async def get_awsaccount(request: web.Request) -> web.Response:
    """
    Gets the AWS account with the given id. If no AWS credentials can be found, it uses any credentials found by the
    AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    id_ = request.match_info['id']
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting AWS account {id_}',
                                                activity_cb=publish_desktop_object) as activity:
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'id^{request.match_info["id"]}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        include_data = True
        if cached_value is not None:
            account_dict, volume_id, permissions, attribute_permissions = cached_value
        else:
            if include_data := parse_bool(request.query.get('data') or 'true'):
                account, volume_id = await _get_awsaccount_by_aws_account_id(request, id_)
                logger.debug('Got account %s and volume %s', account, volume_id)
                if account is None:
                    raise response.status_not_found()
                context = AWSAccountPermissionContext(request, volume_id)
                share = await account.get_permissions_as_share(context)
                permissions = share.permissions
                attribute_permissions = await account.get_all_attribute_permissions(context)
                account.shares = [share]
                account_dict = account.to_dict()
                request.app[HEA_CACHE][cache_key] = (account_dict, volume_id, permissions, attribute_permissions)
                request.app[HEA_CACHE][(sub, f'volume_id^{volume_id}')] = (account_dict, volume_id, permissions, attribute_permissions)
            else:
                volume_id = await _get_volume_by_aws_account_id(request, id_)
                account_dict = {'id': id_, 'type': AWSAccount.get_type_name()}
                permissions = None
                attribute_permissions = None
        request.match_info['volume_id'] = volume_id
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_id = id_
        activity.new_object_uri = f'awsaccounts/{id_}'
        activity.new_volume_id = volume_id
        return await response.get(request, account_dict,
                                  permissions=permissions,
                                  attribute_permissions=attribute_permissions,
                                  include_data=include_data)


@routes.get('/awsaccounts/byname/{name}')
@action('heaserver-accounts-awsaccount-get-self', rel='self hea-account', path='awsaccounts/{id}')
@action(name='heaserver-accounts-awsaccount-get-volume', rel='hea-volume', path='volumes/{volume_id}')
async def get_awsaccount_by_name(request: web.Request) -> web.Response:
    """
    Gets the AWS account with the given id. If no AWS credentials can be found, it uses any credentials found by the
    AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    name = request.match_info['name']
    sub = request.headers.get(SUB, NONE_USER)

    async with DesktopObjectActionLifecycle(request=request,
                                                    code='hea-get',
                                                    description=f'Getting AWS account {name}',
                                                    activity_cb=publish_desktop_object) as activity:
        cache_key = (sub, f'id^{name}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            account, volume_id, permissions, attribute_permissions = cached_value
        else:
            account, volume_id = await _get_account_by_name(request)
            request.match_info['volume_id'] = volume_id
            if account is None:
                raise response.status_not_found()
            context = AWSAccountPermissionContext(request, volume_id)
            share = await account.get_permissions_as_share(context)
            permissions = share.permissions
            attribute_permissions = await account.get_all_attribute_permissions(context)
            account.shares = [share]
            request.app[HEA_CACHE][cache_key] = (account, volume_id, permissions, attribute_permissions)
            request.app[HEA_CACHE][(sub, f'volume_id^{volume_id}')] = (account, volume_id, permissions, attribute_permissions)
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_id = name
        activity.new_object_uri = f'awsaccounts/{name}'
        activity.new_volume_id = volume_id
    return await response.get(request, account.to_dict(), permissions=permissions, attribute_permissions=attribute_permissions)


@routes.get('/awsaccounts')
@routes.get('/awsaccounts/')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu', path='awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-self', rel='self', path='awsaccounts/{id}')
async def get_awsaccounts(request: web.Request) -> web.Response:
    """
    Gets all AWS accounts. If no AWS credentials can be found, it uses any credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: a Response object with the requested AWS accounts or the empty list
    ---
    summary: The user's AWS accounts.
    tags:
        - heaserver-accounts-awsaccount
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting all AWS accounts',
                                                activity_cb=publish_desktop_object) as activity:
        account_ids: list[str] = request.query.getall('account_id', [])
        accounts, _, permissions, attribute_permissions = await _aws_account_ids_to_aws_accounts(request, account_ids)
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_uri = 'awsaccounts/'
        return await response.get_all(request, [a.to_dict() for a in accounts],
                                      permissions=permissions,
                                      attribute_permissions=attribute_permissions)


@routes.get('/volumes/{volume_id}/awsaccounts/me')
@action('heaserver-accounts-awsaccount-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='volumes/{volume_id}/awsaccounts/me/opener')
@action('heaserver-accounts-awsaccount-get-properties', rel='hea-properties hea-context-menu')
@action('heaserver-accounts-awsaccount-get-create-choices', rel='hea-creator-choices hea-context-menu', path='awsaccounts/{id}/creator')
@action('heaserver-accounts-awsaccount-get-trash', rel='hea-trash hea-context-menu', path='volumes/{volume_id}/awss3trash')
@action('heaserver-accounts-awsaccount-get-self', rel='self hea-account', path='awsaccounts/{id}')
@action(name='heaserver-accounts-awsaccount-get-volume', rel='hea-volume', path='volumes/{volume_id}')
async def get_awsaccount_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets the AWS account associated with the given volume id. If the volume's credentials are None, it uses any
    credentials found by the AWS boto3 library.

    :param request: the HTTP request.
    :return: the requested AWS account or Not Found.
    ---
    summary: The user's AWS account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting my AWS account',
                                                activity_cb=publish_desktop_object) as activity:
        volume_id = request.match_info['volume_id']
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'volume_id^{volume_id}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            account, volume_id, permissions, attribute_permissions = cached_value
        else:
            account = await _get_awsaccount_by_volume_id(request, volume_id)
            if account is None:
                raise response.status_not_found()
            context = AWSAccountPermissionContext(request, volume_id)
            share = await account.get_permissions_as_share(context)
            permissions = share.permissions
            attribute_permissions = await account.get_all_attribute_permissions(context)
            account.shares = [share]
            request.app[HEA_CACHE][cache_key] = (account, volume_id, permissions, attribute_permissions)
            request.app[HEA_CACHE][(sub, f'id^{account.id}')] = (account, volume_id, permissions, attribute_permissions)
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_volume_id = volume_id
        activity.new_object_uri = f'volumes/{account.id}'
        activity.new_object_id = account.id
        return await response.get(request, account.to_dict(), permissions=permissions,
                                  attribute_permissions=attribute_permissions)


@routes.get('/awsaccounts/{id}/opener')
@action('heaserver-accounts-awsaccount-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='volumes/{volume_id}/bucketitems/')
@action('heaserver-accounts-awsaccount-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='volumes/{volume_id}/storage/')
async def get_awsaccount_opener(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    id_ = request.match_info['id']
    sub = request.headers.get(SUB, NONE_USER)
    cache_key = (sub, f'id^{id_}')
    cached_value = request.app[HEA_CACHE].get(cache_key)
    async with DesktopObjectActionLifecycle(request=request,
                                                    code='hea-get',
                                                    description=f'Accessing AWS account {id_}',
                                                    activity_cb=publish_desktop_object) as activity:
        if cached_value is not None:
            _, volume_id, _, _ = cached_value
        else:
            volume_id = await _get_volume_by_aws_account_id(request, id_)
            if volume_id is None:
                raise response.status_not_found()
        request.match_info['volume_id'] = volume_id  # Needed to make the actions work.
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_uri = f'awsaccounts/{id_}'
        activity.new_object_id = id_
        activity.new_volume_id = volume_id
        return await response.get_multiple_choices(request)


@routes.get('/volumes/{volume_id}/awsaccounts/me/opener')
@action('heaserver-accounts-awsaccount-open-buckets',
        rel=f'hea-opener hea-context-aws hea-default {AWSBucket.get_mime_type()}', path='volumes/{volume_id}/bucketitems/')
@action('heaserver-accounts-awsaccount-open-storage',
        rel=f'hea-opener hea-context-aws {AWSStorage.get_mime_type()}', path='volumes/{volume_id}/storage/')
async def get_awsaccount_opener_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets choices for opening an AWS account.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: AWS account opener choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info['volume_id']
    id_ = request.match_info['id']
    sub = request.headers.get(SUB, NONE_USER)

    async with DesktopObjectActionLifecycle(request=request,
                                                    code='hea-get',
                                                    description=f'Getting my AWS account',
                                                    activity_cb=publish_desktop_object) as activity:
        cache_key = (sub, f'id^{id_}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            account, volume_id, _, _ = cached_value
        else:
            account = await _get_awsaccount_by_volume_id(request, volume_id)
            if account is None:
                raise response.status_not_found()
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_uri = f'awsaccounts/{account.id}'
        activity.new_volume_id = volume_id
        activity.new_object_id = account.id
        return await response.get_multiple_choices(request)


# @routes.post('/volumes/{volume_id}/awsaccounts/me')
# async def post_account_awsaccounts(request: web.Request) -> web.Response:
#     """
#     Posts the awsaccounts information given the correct access key and secret access key.
#
#     :param request: the HTTP request.
#     :return: the requested awsaccounts or Not Found.
#
#     FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
#     """
#     return await awsservicelib.post_account(request)


# @routes.put('/volumes/{volume_id}/awsaccounts/me')
# async def put_account_awsaccounts(request: web.Request) -> web.Response:
#     """
#     Puts the awsaccounts information given the correct access key and secret access key.

#     :param request: the HTTP request.
#     :return: the requested awsaccounts or Not Found.
#     """
#     volume_id = request['volume_id']
#     alt_contact_type = request.match_info.get("alt_contact_type", None)
#     email_address = request.match_info.get("email_address", None)
#     name = request.match_info.get("name", None)
#     phone = request.match_info.get("phone", None)
#     title = request.match_info.get("title", None)

#     async with DesktopObjectActionLifecycle(request=request,
#                                                 code='hea-delete',
#                                                 description=f'Updating my AWS account',
#                                                 activity_cb=publish_desktop_object) as activity:
#         activity.old_object_type_name = AWSAccount.get_type_name()
#         activity.old_object_uri = f'volumes/{volume_id}/awsaccounts/me'
#         activity.old_volume_id = volume_id
#         try:
#             async with aws.AccountClientContext(request, volume_id) as acc_client:
#                 async with aws.STSClientContext(request, volume_id) as sts_client:
#                     def do() -> str:
#                         account_id = sts_client.get_caller_identity().get('Account')
#                         acc_client.put_alternate_contact(AccountId=account_id, AlternateContactType=alt_contact_type,
#                                                         EmailAddress=email_address, Name=name, PhoneNumber=phone, Title=title)
#                         return account_id
#                     account_id = await get_running_loop().run_in_executor(None, do)
#                     sub = request.headers.get(SUB, NONE_USER)
#                     request.app[HEA_CACHE].pop((sub, f'volume_id^{volume_id}'), None)
#                     request.app[HEA_CACHE].pop((sub, f'id^{account_id}'), None)
#                     keys_to_delete = []
#                     for key in request.app[HEA_CACHE]:
#                         if key[1] is None:
#                             keys_to_delete.append(key)
#                     for key in keys_to_delete:
#                         request.app[HEA_CACHE].pop(key, None)
#                     activity.new_object_type_name = AWSAccount.get_type_name()
#                     activity.new_object_uri = f'volumes/{volume_id}/awsaccounts/me'
#                     activity.new_volume_id = volume_id
#             return web.HTTPNoContent()
#         except BotoClientError as e:
#             activity.status = Status.FAILED
#             return web.HTTPBadRequest()


# @routes.delete('/volumes/{volume_id}/awsaccounts/me')
# async def delete_account_awsaccounts(request: web.Request) -> web.Response:
#     """
#     Deletes the awsaccounts information given the correct access key and secret access key.

#     :param request: the HTTP request.
#     :return: the requested awsaccounts or Not Found.

#     FIXME: should only be permitted by an AWS organization administrator, I would think. Need to sort out what the call looks like.
#     """
#     return response.status_not_found()


@routes.get('/awsaccounts/{id}/creator')
async def get_account_creator(request: web.Request) -> web.Response:
    """
        Gets account creator choices.

        :param request: the HTTP Request.
        :return: A Response object with a status of Multiple Choices or Not Found.
        ---
        summary: Account creator choices
        tags:
            - heaserver-accounts-awsaccount
        parameters:
            - $ref: '#/components/parameters/id'
        responses:
          '300':
            $ref: '#/components/responses/300'
          '404':
            $ref: '#/components/responses/404'
        """
    id_ = request.match_info['id']
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting AWS account {id_}',
                                                activity_cb=publish_desktop_object) as activity:
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'id^{request.match_info["id"]}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is None:
            volume_id = await awsservicelib.get_volume_id_for_account_id(request)
        else:
            _, volume_id, _, _ = cached_value
        if volume_id is None:
            raise response.status_not_found()
        activity.new_object_id = id_
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_uri = f'awsaccounts/{id_}'
        activity.new_volume_id = volume_id
        await _add_create_bucket_action(request, volume_id)
        return await response.get_multiple_choices(request)


@routes.get('/volumes/{volume_id}/awsaccounts/me/creator')
async def get_account_creator_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets account creator choices.

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Account creator choices
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting my AWS account',
                                                activity_cb=publish_desktop_object) as activity:
        volume_id = request.match_info["volume_id"]
        async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description="Getting user's AWS account",
                                                activity_cb=publish_desktop_object) as activity:
            sub = request.headers.get(SUB, NONE_USER)
            cache_key = (sub, f'volume_id^{volume_id}')
            cached_value = request.app[HEA_CACHE].get(cache_key)
            if cached_value is not None:
                account, _, _, _ = cached_value
            else:
                account = await _get_awsaccount_by_volume_id(request, volume_id)
                if account is None:
                    raise response.status_not_found()
            activity.new_object_type_name = AWSAccount.get_type_name()
            activity.new_object_uri = f'awsaccounts/{account.id}'
            activity.new_volume_id = volume_id
            activity.new_object_id = account.id
            await _add_create_bucket_action(request, volume_id)
            return await response.get_multiple_choices(request)


@routes.get('/volumes/{volume_id}/awsaccounts/me/newbucket')
@routes.get('/volumes/{volume_id}/awsaccounts/me/newbucket/')
@action('heaserver-accounts-awsaccount-new-bucket-form')
async def get_new_bucket_form_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current bucket, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_id = request.match_info["volume_id"]
    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-get',
                                            description="Getting user's AWS account",
                                            activity_cb=publish_desktop_object) as activity:
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'volume_id^{volume_id}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            account_dict, _, permissions, attribute_permissions = cached_value
        else:
            account = await _get_awsaccount_by_volume_id(request, volume_id)
            if account is None:
                return response.status_not_found()
            context = AWSAccountPermissionContext(request, volume_id)
            share = await account.get_permissions_as_share(context)
            permissions = share.permissions
            attribute_permissions = await account.get_all_attribute_permissions(context)
            account_dict = account.to_dict()
            request.app[HEA_CACHE][cache_key] = (account_dict, volume_id, permissions, attribute_permissions)
            request.app[HEA_CACHE][(sub, f'id^{account.id}')] = (account_dict, volume_id, permissions, attribute_permissions)
        activity.new_object_id = account_dict['id']
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_volume_id = volume_id
        activity.new_object_uri = f'awsaccounts/{account_dict["id"]}'
        return await response.get(request, account_dict,
                                  permissions=permissions,
                                  attribute_permissions=attribute_permissions)


@routes.get('/awsaccounts/{id}/newbucket')
@routes.get('/awsaccounts/{id}/newbucket/')
@action('heaserver-accounts-awsaccount-new-bucket-form')
async def get_new_bucket_form(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current bucket, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    id_ = request.match_info['id']
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-get',
                                                description=f'Getting AWS account {id_}',
                                                activity_cb=publish_desktop_object) as activity:
        sub = request.headers.get(SUB, NONE_USER)
        cache_key = (sub, f'id^{request.match_info["id"]}')
        cached_value = request.app[HEA_CACHE].get(cache_key)
        if cached_value is not None:
            account, volume_id, permissions, attribute_permissions = cached_value
        else:
            account, volume_id = await _get_awsaccount_by_aws_account_id(request, id_)
            if account is None:
                return response.status_not_found()
            context = AWSAccountPermissionContext(request, volume_id)
            share = await account.get_permissions_as_share(context)
            account.shares = [share]
            permissions = share.permissions
            attribute_permissions = await account.get_all_attribute_permissions(context)
            request.app[HEA_CACHE][cache_key] = (account, volume_id, permissions, attribute_permissions)
        activity.new_object_id = id_
        activity.new_object_type_name = AWSAccount.get_type_name()
        activity.new_object_uri = f'awsaccounts/{id_}'
        activity.new_volume_id = volume_id
        return await response.get(request, account.to_dict(), permissions=permissions,
                                  attribute_permissions=attribute_permissions)


@routes.post('/volumes/{volume_id}/awsaccounts/me/newbucket')
@routes.post('/volumes/{volume_id}/awsaccounts/me/newbucket/')
async def post_new_bucket_by_volume_id(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current account, with a template for creating a bucket or Not Found if the requested account does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    requestBody:
        description: A new bucket.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "my-bucket"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.bucket.AWSBucket"
                      },
                      {
                        "name": "region",
                        "value": "us-west-1"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "my-bucket",
                    "type": "heaobject.bucket.AWSBucket",
                    "region": "us-west-1"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-create',
                                                description=f'Creating a new bucket in my AWS account',
                                                activity_cb=publish_desktop_object) as activity:
        logger = logging.getLogger(__name__)
        volume_id = request.match_info['volume_id']
        bucket_url = await type_to_resource_url(request, AWSBucket)
        if bucket_url is None:
            raise ValueError('No AWSBucket service registered')
        headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
        resource_base = str(URL(bucket_url) / volume_id / 'buckets')
        bucket = await new_heaobject_from_type(request, type_=AWSBucket)
        try:
            id_ = await client.post(request.app, resource_base, data=bucket, headers=headers)
            keys_to_delete = []
            for key in request.app[HEA_CACHE]:
                if key[1] is None:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                request.app[HEA_CACHE].pop(key, None)
            activity.new_object_id = id_
            activity.new_object_type_name = AWSBucket.get_type_name()
            activity.new_volume_id = volume_id
            activity.new_object_uri = f'volumes/{volume_id}/buckets/{id_}'
            return await response.post(request, id_, resource_base)
        except ClientResponseError as e:
            activity.status = Status.FAILED
            return response.status_generic(status=e.status, body=str(e))
        except ClientError as e:
            activity.status = Status.FAILED
            return response.status_generic(status=500, body=str(e))



@routes.post('/awsaccounts/{id}/newbucket')
@routes.post('/awsaccounts/{id}/newbucket/')
async def post_new_bucket(request: web.Request) -> web.Response:
    """
    Gets form for creating a new bucket in this account.

    :param request: the HTTP request. Required.
    :return: the current account, with a template for creating a bucket or Not Found if the requested account does not
    exist.
    ---
    summary: An account.
    tags:
        - heaserver-accounts-awsaccount
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
        description: A new bucket.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "my-bucket"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.bucket.AWSBucket"
                      },
                      {
                        "name": "region",
                        "value": "us-west-1"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "my-bucket",
                    "type": "heaobject.bucket.AWSBucket",
                    "region": "us-west-1"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    try:
        id_ = request.match_info['id']
    except KeyError as e:
        return response.status_bad_request(str(e))
    async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-create',
                                                description=f'Creating a new bucket in AWS account',
                                                activity_cb=publish_desktop_object) as activity:
        logger = logging.getLogger(__name__)
        volume_id = await awsservicelib.get_volume_id_for_account_id(request)
        if volume_id is None:
            activity.status = Status.FAILED
            return response.status_bad_request(f'Invalid account id {request.match_info["id"]}')
        bucket_url = await type_to_resource_url(request, AWSBucket)
        if bucket_url is None:
            raise ValueError('No AWSBucket service registered')
        headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
        resource_base = str(URL(bucket_url) / volume_id / 'buckets')
        bucket = await new_heaobject_from_type(request, type_=AWSBucket)
        try:
            id_ = await client.post(request.app, resource_base, data=bucket, headers=headers)
            keys_to_delete = []
            for key in request.app[HEA_CACHE]:
                if key[1] is None:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                request.app[HEA_CACHE].pop(key, None)
            activity.new_object_id = id_
            activity.new_object_type_name = AWSBucket.get_type_name()
            activity.new_volume_id = volume_id
            activity.new_object_uri = f'volumes/{volume_id}/buckets/{id_}'
            return await response.post(request, id_, resource_base)
        except ClientResponseError as e:
            activity.status = Status.FAILED
            return response.status_generic(status=e.status, body=e.message)
        except ClientError as e:
            activity.status = Status.FAILED
            return response.status_generic(status=500, body=str(e))


def main() -> None:
    config = init_cmd_line(description='Manages account information',
                           default_port=8080)
    start(package_name='heaserver-accounts', db=aws.S3Manager,
          wstl_builder_factory=builder_factory(__package__), config=config)


async def _get_awsaccount_by_volume_id(request: Request, volume_id: str) -> AWSAccount:
    """
    Gets the AWS account associated with the provided volume id.

    Only get since you can't delete or put id information
    currently being accessed. If organizations get included, then the delete, put, and post will be added for name,
    phone, email, ,etc.
    NOTE: maybe get email from the login portion of the application?

    :param request: the aiohttp Request (required).
    :param volume_id: the id string of the volume representing the user's AWS account.
    :return: an HTTP response with an AWSAccount object in the body.
    FIXME: a bad volume_id should result in a 400 status code; currently has status code 500.
    """
    return await request.app[HEA_DB].get_account(request, volume_id)


async def _get_awsaccount_by_aws_account_id(request: web.Request, aws_account_id: str) -> tuple[AWSAccount | None, str | None]:
    """
    Gets an account by its id and the account's volume id. The id is expected to be in the request object's match_info
    mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: a two-tuple containing an AWSAccount dict and volume id, or None if no account was found.
    """
    db = request.app[HEA_DB]
    async for volume in db.get_volumes(request, AWSFileSystem, account_ids=[f'{AWSAccount.get_type_name()}^{aws_account_id}']):
        volume_id = volume.id
        return await db.get_account(request, volume_id), volume_id
    return (None, None)


async def _get_volume_by_aws_account_id(request: web.Request, aws_account_id: str) -> str | None:
    """
    Gets an account's volume id. The id is expected to be in the request object's match_info mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: the volume id, or None if no account was found.
    """
    db = request.app[HEA_DB]
    async for volume in db.get_volumes(request, AWSFileSystem, account_ids=[f'{AWSAccount.get_type_name()}^{aws_account_id}']):
        return volume.id
    return None



async def _get_account_by_name(request: web.Request) -> tuple[AWSAccount | None, str | None]:
    """
    Gets an account by its id and the account's volume id. The id is expected to be the request object's match_info
    mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: a two-tuple containing an AWSAccount and volume id, or None if no account was found.
    """
    db = request.app[HEA_DB]
    volume_ids = [volume.id async for volume in db.get_volumes(request, AWSFileSystem)]
    try:
        return await anext((a, v) async for a, v in db.get_accounts(request, volume_ids) if a.name == request.match_info['name'])
    except StopAsyncIteration:
        return (None, None)


async def _post_account(request: Request) -> Response:
    """
    Called this create since the put, get, and post account all handle information about accounts, while create and delete handle creating/deleting new accounts

    account_email (str)     : REQUIRED: The email address of the owner to assign to the new member account. This email address must not already be associated with another AWS account.
    account_name (str)      : REQUIRED: The friendly name of the member account.
    account_role (str)      : If you don't specify this parameter, the role name defaults to OrganizationAccountAccessRole
    access_to_billing (str) : If you don't specify this parameter, the value defaults to ALLOW

    source: https://github.com/aws-samples/account-factory/blob/master/AccountCreationLambda.py

    Note: Creates an AWS account that is automatically a member of the organization whose credentials made the request.
    This is an asynchronous request that AWS performs in the background. Because CreateAccount operates asynchronously,
    it can return a successful completion message even though account initialization might still be in progress.
    You might need to wait a few minutes before you can successfully access the account
    The user who calls the API to create an account must have the organizations:CreateAccount permission

    When you create an account in an organization using the AWS Organizations console, API, or CLI commands, the information required for the account to operate as a standalone account,
    such as a payment method and signing the end user license agreement (EULA) is not automatically collected. If you must remove an account from your organization later,
    you can do so only after you provide the missing information.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html#Organizations.Client.create_account

    You can only close an account from the Billing and Cost Management Console, and you must be signed in as the root user.
    """
    try:
        volume_id = request.match_info.get("volume_id", None)
        account_email = request.match_info.get("account_email", None)
        account_name = request.match_info.get("account_name", None)
        account_role = request.match_info.get("account_role", None)
        access_to_billing = request.match_info.get("access_to_billing", None)
        if not volume_id:
            return web.HTTPBadRequest(body="volume_id is required")
        if not account_email:
            return web.HTTPBadRequest(body="account_email is required")
        if not account_name:
            return web.HTTPBadRequest(body="account_name is required")
        if not account_role:
            return web.HTTPBadRequest(body="account_role is required")
        if not access_to_billing:
            return web.HTTPBadRequest(body="access_to_billing is required")

        def is_iam_user_access_to_billing_type(val: str) -> TypeGuard[IAMUserAccessToBillingType]:
            return val in get_args(IAMUserAccessToBillingType)
        if not is_iam_user_access_to_billing_type(access_to_billing):
            return web.HTTPBadRequest(body="access_to_billing may be ALLOW or DENY")

        async with aws.OrganizationsClientContext(request, volume_id) as org_client:
            org_client.create_account(Email=account_email, AccountName=account_name, RoleName=account_role,
                                      IamUserAccessToBilling=access_to_billing)
            return web.HTTPAccepted()
            # time.sleep(60)        # this is here as it  takes some time to create account, and the status would always be incorrect if it went immediately to next lines of code
            # account_status = org_client.describe_create_account_status(CreateAccountRequestId=create_account_response['CreateAccountStatus']['Id'])
            # if account_status['CreateAccountStatus']['State'] == 'FAILED':    # go to boto3 link above to see response syntax
            #     web.HTTPBadRequest()      # the response syntax contains reasons for failure, see boto3 link above to see possible reasons
            # else:
            #     return web.HTTPCreated()  # it may not actually be created, but it likely isn't a failure which means it will be created after a minute or two more, see boto3 docs
    except BotoClientError as e:
        return web.HTTPBadRequest()  # see boto3 link above to see possible  exceptions


async def _aws_account_ids_to_aws_accounts(request: web.Request, aws_account_ids: Sequence[str], calc_permissions=True) -> tuple[list[AWSAccount], list[str], list[list[Permission]], list[dict[str, list[Permission]]]]:
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    cache_key = (sub, None, tuple(aws_account_ids), calc_permissions)
    cache_value = request.app[HEA_CACHE].get(cache_key) if aws_account_ids is None else None
    if cache_value is None:
        db = request.app[HEA_DB]
        accounts = []
        volume_ids = [volume.id async for volume in db.get_volumes(request, AWSFileSystem, account_ids=tuple(f'{AWSAccount.get_type_name()}^{a}' for a in aws_account_ids))]
        logger.debug('Checking volumes %s for accounts %s', volume_ids, aws_account_ids)
        account_id_to_account = {}
        permissions = []
        attribute_permissions = []
        async for aws_account, volume_id in db.get_accounts(request, volume_ids):
            if not aws_account_ids or aws_account.id in aws_account_ids:
                account_id_to_account[aws_account.id] = aws_account
                if calc_permissions:
                    context = AWSAccountPermissionContext(request, volume_id)
                    share = await aws_account.get_permissions_as_share(context)
                    aws_account.shares = [share]
                    permissions.append(share.permissions)
                    attribute_permissions_obj = await aws_account.get_all_attribute_permissions(context)
                    attribute_permissions.append(attribute_permissions_obj)
                    request.app[HEA_CACHE][(sub, f'id^{aws_account.id}')] = (aws_account, volume_id,
                                                                             permissions, attribute_permissions_obj)
        accounts = list(account_id_to_account.values())
        request.app[HEA_CACHE][cache_key] = (accounts, volume_ids, permissions, attribute_permissions)
    else:
        accounts, volume_ids, permissions, attribute_permissions = cache_value
    return accounts, volume_ids, permissions, attribute_permissions

from heaserver.service.db.awsaction import S3_CREATE_BUCKET

class _S3BucketPermissionContext(AWSPermissionContext[AWSBucket]):
    def __init__(self, request: Request, volume_id: str, **kwargs):
        super().__init__(request=request, volume_id=volume_id, actions=[S3_CREATE_BUCKET], **kwargs)

    def _caller_arn(self, obj: AWSBucket):
        return f'arn:aws:s3:::{obj.bucket_id}'


async def _add_create_bucket_action(request: web.Request, volume_id: str):
    # sub = request.headers.get(SUB, NONE_USER)
    bucket_component = await client.get_component(request.app, AWSBucket)
    assert bucket_component is not None, 'bucket_component cannot be None'
    bucket_resource = bucket_component.get_resource(AWSBucket.get_type_name())
    assert bucket_resource is not None, 'bucket_resource cannot be None'
    # context = _S3BucketPermissionContext(request, volume_id)
    if True:  # (not bucket_resource.manages_creators or bucket_resource.is_creator_user(sub)) and await context.has_creator_permissions(context):
        add_run_time_action(request, 'heaserver-accounts-awsaccount-create-bucket',
                                    rel='hea-creator hea-default application/x.bucket',
                                    path=f'volumes/{volume_id}/awsaccounts/me/newbucket')
