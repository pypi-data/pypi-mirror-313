from typing import Optional, TypedDict, List, Any
from bruce_models import BruceApi

class JEntityInternal(TypedDict):
    """
    Represents the Nextspace internal properties defined under the 'Bruce' key of an Entity record.
    """

    # ID of the entity.
    # If unset an ID will be generated during the Update request.
    ID: Optional[str]
    # Name of the Entity.
    # This can be set directly, or the Entity Type can be configured to use a specific attribute.
    # If the attribute is changed, a re-index should be launched to update the name.
    Name: Optional[str]
    # Nextspace internal ID.
    # Readonly and created on Entity creation.
    InternalID: Optional[int]

    # Entity Type ID.
    EntityType_ID: str

    # ID of the user who created the entity.
    # Will be set automatically on creation.
    CreatedBy_User_ID: Optional[str]
    # Created date/time of the entity.
    CreatedTime: Optional[Any]
    # Array of associated tags (Used to be called layers).
    # Update to change what tags are associated. Exclude from data to keep it the same.
    Layer_ID: Optional[List[int]]

    # Scenario this is related to. Typically the Key, but if the record isn't found then it will be the ID.
    # When present, this indicates this is a variant of the primary record and not the primary record.
    Scenario: Optional[str | int]

    # If we're retrieving historic records, then these values are populated,
    # to indicate the historic data key and date-time.
    HistoricAttrKey: Optional[str]
    HistoricDateTime: Optional[str]
    
    # Marker that indicates the entity is a calculated alternative schema.
    # This is used to indicate that the entity is read-only and should not be saved.
    SchemaID: Optional[str]

    # Entity relative position to parent within an assembly.
    AssemblyPosition: Optional[List[List[float]]]

    # Entity location in degrees/meters.
    # This is typically relative to the active scene's terrain.
    # However what its relative to is dictated by the Entity Style during rendering.
    # This dictates where 3D models are placed, in the absence of VectorGeometry-
    #this is used to place vector points as well.
    Location: Optional[Any]
    # These are applied only to the Entity's LOD and not the VectorGeometry.
    Transform: Optional[Any]
    # Entity boundaries in degrees/meters.
    Boundaries: Optional[Any]
    # Entity vector geometry. Eg: a point, polyline, or polygon to draw.
    VectorGeometry: Optional[Any]

class Entity:
    """
    Represents an Entity in Nextspace.
    You will find the JEntity data-model and all related API communication here.
    """

    class JEntity(TypedDict, total=False):
        """
        Represents the JSON structure of an Entity.
        """
        Bruce: JEntityInternal
        __additional__: Optional[dict[str, Any]]

    @staticmethod
    def get(api: BruceApi, entity_id: str = "") -> JEntity:
        """
        Retrieves an Entity by its ID.
        """
        if not entity_id:
            raise ValueError("A valid Entity ID is required.")
        return api.GET(f"v3/entity/{entity_id}")
    
    @staticmethod
    def get(api: BruceApi, entity_id: str = "", scenario: Optional[str | int] = 0) -> JEntity:
        """
        Retrieves an Entity by its ID and Scenario.
        """
        if not entity_id:
            raise ValueError("A valid Entity ID is required.")
        return api.GET(f"v3/entity/{entity_id}?Scenario={scenario}")
    
    @staticmethod
    def get_list(
        api: BruceApi, 
        entity_type_id: str = "", 
        skip: int = 0, 
        take: int = 50,
        scenario: Optional[str | int] = 0
    ) -> List[JEntity]:
        """
        Retrieves a list of Entities.
        """
        params = {
            "Type": entity_type_id,
            "PageIndex": skip,
            "PageSize": take,
            "Scenario": scenario
        }
        data = api.GET("v3/entities", params)
        return data["Items"]
    
    @staticmethod
    def update(
        api: BruceApi,
        # Entity to update/create.
        entity: JEntityInternal, 
        # (Optional) Scenario to update the Entity under.
        # It can be specified here, or within the Entity itself.
        # If specified here, it will override the Entity's Scenario.
        scenario: Optional[str | int] = 0
    ) -> JEntity:
        """
        Updates or creates an Entity.
        If an Entity does not have an ID, a new record is made.
        """
        params = {
            "Scenario": scenario
        }
        return api.POST("v3/entity", entity, params)
    
    @staticmethod
    def update_list(
        api: BruceApi,
        # List of Entities to update/create.
        entities: List[JEntityInternal], 
        # (Optional) Scenario to update the Entities under.
        # It can be specified here, or within the Entity itself.
        # If specified here, it will override the Entity's Scenario.
        scenario: Optional[str | int] = 0
    ) -> List[JEntity]:
        """
        Updates or creates a list of Entities.
        If an Entity does not have an ID, a new record is made.
        """
        body = {
            "Items": entities,
            "Scenario": scenario
        }
        data = api.POST("v3/entities", body)
        return data["Items"]