from typing import Optional, TypedDict, List, Any
from bruce_models import BruceApi

class EntityType:
    """
    Represents an Entity Type in Nextspace.
    You will find the JEntityType data-model and all related API communication here.
    """

    class JEntityType(TypedDict):
        # ID of the Entity Type.
        ID: Optional[str]
        # Human readable name of the Entity Type.
        Name: str;
        # Human readable description of the Entity Type.
        Description: Optional[str]
        # If Entity Type access (and Entity access) should be restricted.
        # When an Entity Type is restricted a user must have the "EntityType_<typeId>" permission.
        IsAccessRestricted: Optional[bool]
        # The data schema defining expected attributes for entities to have.
        DataSchema: Optional[Any]
        # Attribute that defines Entity names in the Entity Type.
        # If not supplied, then the Entities can have names set directly.
        # It is a comma separated array of attribute string paths.
        DisplayNameAttributePath: Optional[str]
        # If this schema is "strict". If Entities in an Entity Type are different enough between each-other then the schema is not strict.
        # This will dictate how UI will display the attributes.
        IsStrictSchema: Optional[bool]
        # Default Style for the corresponding Entities.
        DisplaySettings_ID: Optional[int]
        # Last updated date/time.
        LastUpdate_Time: Optional[Any]
        # ID of the parent Entity Type (if any).
        # This is used for organization. When a parent type is deleted, the child types are also deleted.
        Parent_EntityType_ID: Optional[str]

    @staticmethod
    def get(api: BruceApi, id: str) -> JEntityType:
        """
        Get an Entity Type by its ID.
        """
        if not id:
            raise ValueError("ID is required to get an Entity Type.")
        return api.GET("entitytype", id)
    
    @staticmethod
    def get_list(api: BruceApi) -> List[JEntityType]:
        """
        Get a list of all Entity Types.
        """
        data = api.GET("entitytypes")
        return data["Items"]