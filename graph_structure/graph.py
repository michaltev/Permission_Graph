import jsonlines

from graph_structure.edge import Edge, ParentEdge, RoleEdge
from graph_structure.node import Node, IdentityNode, ResourceNode, \
    generate_resource_id, generate_resource_asset_type, generate_identity_id_type


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.root_resource = {}

    def __get_resources_by_identity(self, p_identity_id: str):
        return [edge for edge in self.edges if
                type(edge) is RoleEdge and edge.from_node.id == p_identity_id]

    def __get_parent_by_resource(self, p_node_id: str):
        return [edge.from_node.id for edge in self.edges if
                type(edge) is ParentEdge and edge.to_node.id == p_node_id][0]

    def __get_identities_by_resource(self, p_resource_id: str):
        return [edge for edge in self.edges if
                type(edge) is RoleEdge and edge.to_node.id == p_resource_id]

    def __create_identities_relationships(self, p_curr_resource_node, lst_bindings):
        for binding in lst_bindings:
            role = binding["role"]
            lst_identities = binding["members"]

            for identity_str in lst_identities:
                identity_id, identity_type = generate_identity_id_type(identity_str)
                # creates identities nodes
                identity_node = IdentityNode(identity_id, identity_type)
                self.add_node(identity_node)

                # creates role-edge to each identity
                role_edge = RoleEdge(identity_node, p_curr_resource_node, role)
                self.add_edge(role_edge)

    def __create_ancestors_relationships(self, p_curr_resource_node, p_lst_ancestors):
        child_node = p_curr_resource_node
        for i in range(1, len(p_lst_ancestors)):
            # adds the node of the father
            ancestor_id = p_lst_ancestors[i]
            ancestor_node = ResourceNode(ancestor_id)
            self.add_node(ancestor_node)

            # creates the edge between them
            parent_edge = ParentEdge(ancestor_node, child_node)
            self.add_edge(parent_edge)

            # the parent becomes the child of the next ancestor
            child_node = ancestor_node

    def __create_resource_node(self, p_node_id, p_asset_type):
        curr_resource_node = ResourceNode(p_node_id, p_asset_type)
        self.add_node(curr_resource_node)
        return curr_resource_node

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

    def __update_edged_with_node(self, p_node: Node):
        for i, edge in enumerate(self.edges):
            if edge.from_node.id == p_node.id:
                self.edges[i].from_node = p_node
            elif edge.to_node.id == p_node.id:
                self.edges[i].to_node = p_node

    def create_graph(self):
        with jsonlines.open('./data/data_file.json') as reader:
            for line in reader:
                node_id = generate_resource_id(line["name"])
                asset_type = generate_resource_asset_type(line["asset_type"])
                curr_resource_node = self.__create_resource_node(node_id, asset_type)

                if curr_resource_node.asset_type != "Organization":
                    lst_ancestors = line["ancestors"]
                    self.__create_ancestors_relationships(curr_resource_node, lst_ancestors)

                lst_bindings = line["iam_policy"]["bindings"]
                self.__create_identities_relationships(curr_resource_node, lst_bindings)

    def add_node(self, p_node: Node):
        node_index = next((index for (index, node) in enumerate(self.nodes) if node.id == p_node.id), None)
        if node_index:
            curr_node = self.nodes[node_index]
            if (type(curr_node) is ResourceNode) and (type(p_node) is ResourceNode) and \
                    (p_node.asset_type != "") and (curr_node.asset_type != p_node.asset_type):
                self.nodes[node_index] = p_node
                self.__update_edged_with_node(p_node)
        else:
            self.nodes.append(p_node)

        if (type(p_node) is ResourceNode) and (p_node.asset_type == "Organization"):
            self.root_resource = p_node

        return p_node

    def add_edge(self, p_edge: Edge):
        is_exist = next((edge for edge in self.edges if
                         edge.from_node.id == p_edge.from_node.id and
                         edge.to_node.id == p_edge.to_node.id and
                         edge.type == p_edge.type), None)
        if is_exist is None:
            self.edges.append(p_edge)

    def print_relationships(self):
        for edge in self.edges:
            print(edge.from_node.id + "---" + edge.type + "--->" + edge.to_node.id)

    def get_resource_hierarchy(self, p_resource_id: str):
        if self.root_resource.id == p_resource_id:
            return "That was easy! You are searching the root organization"
        path = []
        return self.__get_recursive_hierarchy(p_resource_id, path)

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
