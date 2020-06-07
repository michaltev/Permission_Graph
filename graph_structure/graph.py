import jsonlines

from graph_structure.edge import Edge, ParentEdge, RoleEdge
from graph_structure.node import Node, IdentityNode, ResourceNode, generate_resource_id, generate_resource_asset_type


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.root_resource = {}

    def __get_resources_by_identity(self, p_identity_id: str):
        return [edge for edge in self.edges if
                type(edge) == RoleEdge and edge.from_node.id == p_identity_id]

    def __get_parent_by_resource(self, p_node_id: str):
        return [edge.from_node.id for edge in self.edges if
                type(edge) == ParentEdge and edge.to_node.id == p_node_id][0]

    def __get_identities_by_resource(self, p_resource_id: str):
        return [edge for edge in self.edges if
                type(edge) == RoleEdge and edge.to_node.id == p_resource_id]

    def __get_recursive_hierarchy(self, p_resource_id: str, p_path: list):
        if self.root_resource.id == p_resource_id:
            return p_path
        parent_resource = self.__get_parent_by_resource(p_resource_id)
        p_path.append(parent_resource)

        return self.__get_recursive_hierarchy(parent_resource, p_path)

    def __get_children_resources_bfs(self, p_root_resource: ResourceNode):
        # keep track of all visited nodes
        explored = []
        # keep track of nodes to be checked
        queue = [p_root_resource]

        # keep looping until there are nodes still to be checked
        while queue:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            if node not in explored:
                # add node to list of checked nodes
                explored.append(node)
                neighbours = self.__get_resources_by_identity(node.id)

                # add neighbours of node to queue
                for neighbour in neighbours:
                    queue.append(neighbour)
        return explored
        pass

    def __update_edged_with_node(self, p_node: Node):
        for i, edge in enumerate(self.edges):
            if edge.from_node.id == p_node.id:
                self.edges[i].from_node = p_node
            elif edge.to_node.id == p_node.id:
                self.edges[i].to_node = p_node
        pass

    def create_graph(self):
        with jsonlines.open('./data/data_file.json') as reader:
            for line in reader:
                # creates resource node
                node_id = generate_resource_id(line["name"])
                asset_type = generate_resource_asset_type(line["asset_type"])
                curr_resource_node = ResourceNode(node_id, asset_type)
                self.add_node(curr_resource_node)

                if asset_type != "Organization":
                    lst_ancestors = line["ancestors"]
                    child_node = curr_resource_node

                    for i in range(1, len(lst_ancestors)):
                        # adds the node of the father
                        ancestor_id = lst_ancestors[i]
                        ancestor_node = ResourceNode(ancestor_id)
                        self.add_node(ancestor_node)

                        # creates the edge between them
                        parent_edge = ParentEdge(ancestor_node, child_node)
                        self.add_edge(parent_edge)

                        # the parent becomes the child of the next ancestor
                        child_node = ancestor_node

                lst_bindings = line["iam_policy"]["bindings"]

                for binding in lst_bindings:
                    role = binding["role"]
                    lst_identities = binding["members"]

                    for identity in lst_identities:
                        # creates identities nodes
                        identity_node = IdentityNode(identity)
                        self.add_node(identity_node)

                        # creates role-edge to each identity
                        role_edge = RoleEdge(identity_node, curr_resource_node, role)
                        self.add_edge(role_edge)
        pass

    def add_node(self, p_node: Node):
        node_index = next((index for (index, node) in enumerate(self.nodes) if node.id == p_node.id), None)
        if node_index:
            curr_node = self.nodes[node_index]
            if (hasattr(curr_node, "asset_type")) and \
                    (p_node.asset_type != "") and \
                    (curr_node.asset_type != p_node.asset_type):
                self.nodes[node_index] = p_node
                self.__update_edged_with_node(p_node)
        else:
            self.nodes.append(p_node)

        if (hasattr(p_node, "asset_type")) and (p_node.asset_type == "Organization"):
            self.root_resource = p_node

        return p_node
        pass

    def add_edge(self, p_edge: Edge):
        is_exist = next((edge for edge in self.edges if edge.from_node.id == p_edge.from_node.id and
                         edge.to_node.id == p_edge.to_node.id and
                         edge.type == p_edge.type), None)
        if is_exist is None:
            self.edges.append(p_edge)

        pass

    def print_relationships(self):
        for edge in self.edges:
            print(edge.from_node.id + "---" + edge.type + "--->" + edge.to_node.id)
        pass

    def get_resource_hierarchy(self, p_resource_id: str):
        if self.root_resource.id == p_resource_id:
            return "That was easy! You are searching the root organization"
        path = []
        return self.__get_recursive_hierarchy(p_resource_id, path)
        pass

    def get_user_permissions(self, p_identity_id: str):
        lst_permissions = list()
        # gets all the resources connected to the identity
        for edge in self.__get_resources_by_identity(p_identity_id):
            role = edge.type
            resource_node = edge.to_node
            # bfs all the children of the resource
            lst_children_resources_bfs = self.__get_children_resources_bfs(resource_node)
            for node in lst_children_resources_bfs:
                permission_tuple = (node.id, node.asset_type, role)
                if permission_tuple not in lst_permissions:
                    lst_permissions.append(permission_tuple)

        return lst_permissions
        pass

    def get_resources_permitted(self, p_resource_id: str):
        lst_permitted_identities = []
        # gets all the parents resources of the current resource
        lst_parent_resources = self.get_resource_hierarchy(p_resource_id)
        # adds the current resource to the list of resources
        lst_parent_resources.append(p_resource_id)

        for parent_resource_id in lst_parent_resources:
            # gets all the identities connected to the resource
            for edge in self.__get_identities_by_resource(parent_resource_id):
                identity_tuple = (edge.from_node.id, edge.type)
                if identity_tuple not in lst_permitted_identities:
                    lst_permitted_identities.append(identity_tuple)

        return lst_permitted_identities
        pass
