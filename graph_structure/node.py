class Node:
    def __init__(self, p_id: str, p_type: str):
        self.id = p_id
        self.type = p_type

    pass


class IdentityNode(Node):
    def __init__(self, p_id: str):  # task6 > p_sub_type):
        super().__init__(p_id, "identity")
        # task6 > self.sub_type = p_sub_type

    pass


class ResourceNode(Node):
    def __init__(self, p_id: str, p_asset_type: str = None):
        if p_asset_type:
            self.asset_type = p_asset_type
        else:
            self.asset_type = ""
        super().__init__(p_id, "resource")

    pass


def generate_resource_id(p_name: str):
    lst_name_split = p_name.split("/")
    return lst_name_split[len(lst_name_split) - 2] + "/" + lst_name_split[len(lst_name_split) - 1]
    pass


def generate_resource_asset_type(p_asset_type):
    lst_name_split = p_asset_type.split("/")
    return lst_name_split[len(lst_name_split) - 1]
    pass
