from api.directory_api import DirectoryAPI
from graph_structure.graph import Graph

permission_graph = Graph()
# Task 1
permission_graph.create_graph()
# Task 2
print(permission_graph.get_resource_hierarchy("folders/837642324986"))
# Task 3
# print(permission_graph.get_user_permissions("user:ron@test.authomize.com"))
# print(permission_graph.get_user_permissions("group:reviewers@test.authomize.com"))
# Task 3 after Task 6
print(permission_graph.get_user_permissions("ron@test.authomize.com"))
print(permission_graph.get_user_permissions("reviewers@test.authomize.com"))
# Task 4
print(permission_graph.get_resources_permitted("folders/96505015065"))
# Task 5
google_api = DirectoryAPI()
print(len(google_api.fetch_users_in_organization()))
print(len(google_api.fetch_groups_in_organization()))
print(google_api.fetch_users_in_groups())