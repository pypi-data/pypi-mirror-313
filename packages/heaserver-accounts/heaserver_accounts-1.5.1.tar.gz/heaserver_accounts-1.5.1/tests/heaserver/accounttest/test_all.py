from .testcase import AWSAccountTestCase
from heaserver.service.testcase.mixin import GetAllMixin, GetOneMixin
from heaserver.service.representor import nvpjson
from heaobject.account import AWSAccount
from heaobject.user import AWS_USER, NONE_USER
from heaobject.source import AWS
from heaobject.root import ShareImpl, Permission
from aiohttp import hdrs


# class TestDeleteAccount(AWSAccountTestCase, DeleteMixin):
#     pass
#
#
class TestGetAccounts(AWSAccountTestCase, GetAllMixin):
    pass


class TestGetAccount(AWSAccountTestCase, GetOneMixin):
    def setUp(self):
        account_id = '123456789012'
        self.account = AWSAccount()
        self.account.id = account_id
        self.account.name = 'master'
        self.account.display_name = account_id
        self.account.email_address = 'master@example.com'
        self.account.owner = AWS_USER
        self.account.source = AWS
        self.account.source_detail = AWS
        share = ShareImpl()
        share.permissions = [Permission.VIEWER]
        share.user = NONE_USER
        self.account.shares = [share]

    async def test_get_account_me_status(self):
        async with self.client.request('GET', '/volumes/666f6f2d6261722d71757578/awsaccounts/me') as resp:
            self.assertEqual(200, resp.status)

    async def test_get_account_me(self):
        url = '/volumes/666f6f2d6261722d71757578/awsaccounts/me'
        async with self.client.request('GET', url, headers={hdrs.ACCEPT: nvpjson.MIME_TYPE}) as resp:
            self.assertEqual([self.account.to_dict()], await resp.json())

    async def test_get_new_bucket_form(self):
        url = '/volumes/666f6f2d6261722d71757578/awsaccounts/me/newbucket/'
        expected = [{'collection': {'version': '1.0',
                                    'permissions': [['VIEWER']],
                                    'items': [{'data': [{'name': 'alternate_contact_name', 'value': None, 'prompt': 'alternate_contact_name', 'display': True},
                                                        {'name': 'alternate_email_address', 'value': None, 'prompt': 'alternate_email_address', 'display': True},
                                                        {'name': 'alternate_phone_number', 'value': None, 'prompt': 'alternate_phone_number', 'display': True},
                                                        {'name': 'created', 'value': None, 'prompt': 'created', 'display': True},
                                                        {'name': 'derived_by', 'value': None, 'prompt': 'derived_by', 'display': True},
                                                        {'name': 'derived_from', 'value': [], 'prompt': 'derived_from', 'display': True},
                                                        {'name': 'description', 'value': None, 'prompt': 'description', 'display': True},
                                                        {'name': 'display_name', 'value': '123456789012', 'prompt': 'display_name', 'display': True},
                                                        {'name': 'email_address', 'value': 'master@example.com', 'prompt': 'email_address', 'display': True},
                                                        {'name': 'full_name', 'value': None, 'prompt': 'full_name', 'display': True},
                                                        {'name': 'id', 'value': '123456789012', 'prompt': 'id', 'display': False},
                                                        {'name': 'instance_id', 'value': 'heaobject.account.AWSAccount^123456789012', 'prompt': 'instance_id', 'display': True},
                                                        {'name': 'invites', 'value': [], 'prompt': 'invites', 'display': True},
                                                        {'name': 'mime_type', 'value': 'application/x.awsaccount', 'prompt': 'mime_type', 'display': True},
                                                        {'name': 'modified', 'value': None, 'prompt': 'modified', 'display': True},
                                                        {'name': 'name', 'value': 'master', 'prompt': 'name', 'display': True},
                                                        {'name': 'owner', 'value': 'system|aws', 'prompt': 'owner', 'display': True},
                                                        {'name': 'phone_number', 'value': None, 'prompt': 'phone_number', 'display': True},
                                                        {'name': 'shares', 'value': [], 'prompt': 'shares', 'display': True},
                                                        {'name': 'source', 'value': 'Amazon Web Services', 'prompt': 'source', 'display': True},
                                                        {'name': 'source_detail', 'value': 'Amazon Web Services', 'prompt': 'source_detail', 'display': True},
                                                        {'name': 'type', 'value': 'heaobject.account.AWSAccount', 'prompt': 'type', 'display': True},
                                                        {'name': 'type_display_name', 'value': 'AWS Account', 'prompt': 'type_display_name', 'display': True},
                                                        {'name': 'file_system_type', 'value': 'heaobject.volume.AWSFileSystem', 'prompt': 'file_system_type', 'display': True},
                                                        {'name': 'file_system_name', 'value': 'DEFAULT_FILE_SYSTEM', 'prompt': 'file_system_name', 'display': True},
                                                        {'name': 'credential_type_name', 'value': 'heaobject.keychain.AWSCredentials', 'prompt': 'credential_type_name', 'display': True}],
                                               'links': []}],
                                    'template': {'prompt': 'New Folder', 'rel': '',
                                                 'data': [{'name': 'display_name', 'value': None, 'prompt': 'Name', 'required': True, 'readOnly': True, 'pattern': None},
                                                          {'name': 'type', 'value': 'heaobject.bucket.AWSBucket', 'prompt': 'Type', 'required': True, 'readOnly': True, 'pattern': None, 'display': False},
                                                          {'name': 'region', 'value': None, 'prompt': 'Region', 'required': True, 'readOnly': False, 'pattern': None, 'type': 'select',
                                                           'options': [{'value': 'us-east-2', 'text': 'US East (Ohio)'}, {'value': 'us-east-1', 'text': 'US East (N. Virginia)'}, {'value': 'us-west-1', 'text': 'US West (N. California)'}, {'value': 'us-west-2', 'text': 'US West (Oregon)'}, {'value': 'af-south-1', 'text': 'Africa (Cape Town)'}, {'value': 'ap-east-1', 'text': 'Asia Pacific (Hong Kong)'}, {'value': 'ap-southeast-3', 'text': 'Asia Pacific (Jakarta)'}, {'value': 'ap-south-1', 'text': 'Asia Pacific (Mumbai)'}, {'value': 'ap-northeast-3', 'text': 'Asia Pacific (Osaka)'}, {'value': 'ap-northeast-2', 'text': 'Asia Pacific (Seoul)'}, {'value': 'ap-southeast-1', 'text': 'Asia Pacific (Singapore)'}, {'value': 'ap-southeast-2', 'text': 'Asia Pacific (Sydney)'}, {'value': 'ap-northeast-1', 'text': 'Asia Pacific (Tokyo)'}, {'value': 'ca-central-1', 'text': 'Canada (Central)'}, {'value': 'eu-central-1', 'text': 'Europe (Frankfurt)'}, {'value': 'eu-west-1', 'text': 'Europe (Ireland)'}, {'value': 'eu-west-2', 'text': 'Europe (London)'}, {'value': 'eu-south-1', 'text': 'Europe (Milan)'}, {'value': 'eu-west-3', 'text': 'Europe (Paris)'}, {'value': 'eu-north-1', 'text': 'Europe (Stockholm)'}, {'value': 'me-south-1', 'text': 'Middle East (Bahrain)'}, {'value': 'sa-east-1', 'text': 'South America (São Paulo)'}],
                                                           "value": "us-east-1"},
                                                          {'name': 'versioned', 'options': [{'text': 'True', 'value': 'true'}, {'text': 'False', 'value': 'false'}], 'pattern': None, 'prompt': 'Versioned', 'readOnly': False, 'required': True, 'type': 'select', 'value': 'true'}]}}}]

        async with self.client.request('GET', url) as resp:
            actual = await resp.json()
            del actual[0]['collection']['href']  # The href's port will change every time.
            self._assert_equal_ordered(expected, actual)

#
#
# class TestPutAccount(AWSAccountTestCase, PutMixin):
#     pass
#
#
# class TestPostAccount(AWSAccountTestCase, PostMixin):
#     pass
