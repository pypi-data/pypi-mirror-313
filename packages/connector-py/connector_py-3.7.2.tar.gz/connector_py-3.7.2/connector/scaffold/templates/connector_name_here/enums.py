from enum import Enum

from connector.generated import EntitlementType, ResourceType


class {pascal}ResourceType(str, Enum):
    GLOBAL_RESOURCE = "GLOBAL_RESOURCE"

class {pascal}EntitlementType(str, Enum):
    pass

resource_types = [
    ResourceType(
        type_id={pascal}ResourceType.GLOBAL_RESOURCE,
        type_label="Global Resource",
    )
]

entitlement_types: list[EntitlementType] = []
