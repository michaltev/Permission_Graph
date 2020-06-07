from api.directory_api import DirectoryAPI
from graph_structure.graph import Graph

g = Graph()
# Task 1
g.create_graph()
# Task 2
print(g.get_resource_hierarchy("folders/837642324986"))
# Task 3
print(g.get_user_permissions("user:ron@test.authomize.com"))
print(g.get_user_permissions("group:reviewers@test.authomize.com"))
# Task 4
print(g.get_resources_permitted("folders/837642324986"))
# Task 5
google_api = DirectoryAPI()
google_api.fetch_users_in_organization()
google_api.fetch_groups_in_organization()
google_api.fetch_users_in_groups()
