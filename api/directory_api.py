from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = 'ron@test.authomize.com'

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_JSON_FILE_PATH = 'data/service_account_file.json'


class DirectoryAPI:
    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_JSON_FILE_PATH,
            scopes=['https://www.googleapis.com/auth/admin.directory.user.readonly',
                    'https://www.googleapis.com/auth/admin.directory.group.readonly',
                    'https://www.googleapis.com/auth/admin.directory.group.member.readonly'])

        credentials = credentials.create_delegated(SERVICE_ACCOUNT_EMAIL)

        self.service = build('admin', 'directory_v1', credentials=credentials)

    def fetch_users_in_organization(self):
        results = self.service.users().list(customer='my_customer').execute()
        users = results.get('users', [])
        return users

    def fetch_groups_in_organization(self):
        results = self.service.groups().list(customer='my_customer').execute()
        groups = results.get('groups', [])
        return groups

    def fetch_users_in_groups(self):
        groups = self.fetch_groups_in_organization()
        dict_users_in_groups = {}

        if groups:
            for group in groups:
                group_id = group['id']
                group_name = group['name']
                lst_users_members = self.get_group_members(group_id)
                dict_users_in_groups[group_name] = lst_users_members
        return dict_users_in_groups

    def get_group_members(self, group_id):
        results = self.service.members().list(groupKey=group_id).execute()
        members = results.get('members', [])
        lst_users_members = []
        if members:
            lst_users_members = [member['email'] for member in members if
                                 member['type'] == "USER"]
        return lst_users_members
