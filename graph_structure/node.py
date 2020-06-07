class Node:
    def __init__(self, p_id: str, p_type: str):
        self.id = p_id
        self.type = p_type


class IdentityNode(Node):
    def __init__(self, p_id: str, p_type: str):
        super().__init__(p_id, p_type)


class ResourceNode(Node):
    def __init__(self, p_id: str, p_asset_type: str = None):
        if p_asset_type:
            self.asset_type = p_asset_type
        else:
            self.asset_type = ""
        super().__init__(p_id, "resource")


def generate_resource_id(p_name: str):
    lst_name_split = p_name.split("/")
    return lst_name_split[len(lst_name_split) - 2] + "/" + lst_name_split[len(lst_name_split) - 1]


def generate_resource_asset_type(p_asset_type: str):
    lst_name_split = p_asset_type.split("/")
    return lst_name_split[len(lst_name_split) - 1]


def generate_identity_id_type(p_identity_name: str):
    lst_name_split = p_identity_name.split(":")
    identity_type = lst_name_split[0]
    identity_id = lst_name_split[1]
    return identity_id, identity_type
