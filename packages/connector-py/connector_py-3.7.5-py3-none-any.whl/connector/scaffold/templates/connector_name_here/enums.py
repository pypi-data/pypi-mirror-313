from enum import Enum

from connector.generated import EntitlementType, ResourceType


class {pascal}ResourceTypes(str, Enum):
    GLOBAL_RESOURCE = "GLOBAL_RESOURCE"

class {pascal}EntitlementTypes(str, Enum):
    GLOBAL_ROLE = "Role"

resource_types: list[ResourceType] = [
    ResourceType(
        type_id={pascal}ResourceTypes.GLOBAL_RESOURCE,
        type_label="Global Resource",
    )
]

entitlement_types: list[EntitlementType] = [
    EntitlementType(
        type_id={pascal}EntitlementTypes.GLOBAL_ROLE,
        type_label="Role",
        resource_type_id={pascal}ResourceTypes.GLOBAL_RESOURCE,
        min=0,
        # You can also set a max, if users can't have infinite of these entitlements
        # max=1,
    )
]
