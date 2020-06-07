from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SERVICE_ACCOUNT_EMAIL = 'ron@test.authomize.com'
SERVICE_ACCOUNT_JSON_FILE_PATH = 'data/service_account_file.json'
COSTUMER = "my_customer"


class DirectoryAPI:
    def __init__(self):
        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                SERVICE_ACCOUNT_JSON_FILE_PATH,
                scopes=['https://www.googleapis.com/auth/admin.directory.user.readonly',
                        'https://www.googleapis.com/auth/admin.directory.group.readonly',
                        'https://www.googleapis.com/auth/admin.directory.group.member.readonly'])

            credentials = credentials.create_delegated(SERVICE_ACCOUNT_EMAIL)

            self.service = build('admin', 'directory_v1', credentials=credentials)
        except Exception:
            self.service = {}
            print("An exception occurred")

    def fetch_users_in_organization(self):
        try:
            results = self.service.users().list(customer=COSTUMER).execute()
            users = results.get('users', [])
        except Exception:
            users = []
            print("An exception occurred, no users are fetched")
        return users

    def fetch_groups_in_organization(self):
        try:
            results = self.service.groups().list(customer=COSTUMER).execute()
            groups = results.get('groups', [])
        except Exception:
            groups = []
            print("An exception occurred, no groups are fetched")
        return groups

    def fetch_users_in_groups(self):
        groups = self.fetch_groups_in_organization()
        dict_users_in_groups = {}

        if groups:
            for group in groups:
                group_id = group['id']
                group_email = group['email']
                lst_users_members = self.__get_group_members(group_id)
                dict_users_in_groups[group_email] = lst_users_members
        return dict_users_in_groups

    def __get_group_members(self, group_id):
        try:
            results = self.service.members().list(groupKey=group_id).execute()
            members = results.get('members', [])
        except Exception:
            members = []
            print("An exception occurred, no groups are fetched")
        lst_users_members = []
        if members:
            lst_users_members = [member['email'] for member in members if
                                 member['type'] == "USER"]
        return lst_users_members
