from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = 'ron@test.authomize.com'

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_JSON_FILE_PATH = './authomize-15054614561264767466-5ef86365604b.json'


class DirectoryAPI:
    def __init__(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SERVICE_ACCOUNT_JSON_FILE_PATH,
            scopes=['https://www.googleapis.com/auth/admin.directory.user.readonly',
                    'https://www.googleapis.com/auth/admin.directory.group.readonly',
                    'https://www.googleapis.com/auth/admin.directory.group.member.readonly'])

        credentials = credentials.create_delegated(SERVICE_ACCOUNT_EMAIL)

        self.service = build('admin', 'directory_v1', credentials=credentials)


google_api = DirectoryAPI()


def fetch_users_in_organization():
    # Call the Admin SDK Directory API
    results = google_api.service.users().list(customer='my_customer').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'{0} ({1})'.format(user['primaryEmail'],
                                      user['name']['fullName']))
    pass


def fetch_groups_in_organization():
    # Call the Admin SDK Directory API
    results = google_api.service.groups().list(customer='my_customer').execute()
    groups = results.get('groups', [])

    if not groups:
        print('No groups in the domain.')
    else:
        print('Groups:')
        for group in groups:
            print(u'{0} - {1}({2} members)'.format(group['email'],
                                                   group['name'],
                                                   group['directMembersCount']))
    pass


def fetch_users_in_groups():
    # groups -> members -> member.type -> member.email
    results = google_api.service.groups().list(customer='my_customer').execute()
    groups = results.get('groups', [])

    if not groups:
        print('No groups in the domain')
    else:
        for group in groups:
            print(u'GROUP {0}({1})'.format(group['email'], group['name']))

            results = google_api.service.members().list(groupKey=group['id']).execute()
            members = results.get('members', [])
            if not groups:
                print('No members in the group')
            else:
                for member in members:
                    if member['type'] == "USER":
                        print(u'USER {0} is a member'.format(member['email']))
    pass


fetch_users_in_organization()
fetch_groups_in_organization()
fetch_users_in_groups()
