from graph_structure.node import Node, ResourceNode, IdentityNode


class Edge:
    def __init__(self, p_from_node: Node, p_to_node: ResourceNode, p_type: str):
        self.from_node = p_from_node
        self.to_node = p_to_node
        self.type = p_type

    pass


class ParentEdge(Edge):
    def __init__(self, p_from_node: ResourceNode, p_to_node: ResourceNode):
        super().__init__(p_from_node, p_to_node, "parent of")

    pass


class RoleEdge(Edge):
    def __init__(self, p_from_node: IdentityNode, p_to_node: ResourceNode, p_role_type: str):
        super().__init__(p_from_node, p_to_node, p_role_type)

    pass
