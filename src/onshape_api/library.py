from enum import StrEnum

class SMExtrudeBoundingTypes(StrEnum):
    """Bounding type for an extrusion.
    
    Documentation: <https://cad.onshape.com/FsDoc/library.html#SMExtrudeBoundingType>
    """
    BLIND = "BLIND"
    UP_TO_NEXT = "UP_TO_NEXT"
    UP_TO_SURFACE = "UP_TO_SURFACE"
    UP_TO_BODY = "UP_TO_BODY"
    UP_TO_VERTEX = "UP_TO_VERTEX"

class SMNewBodyOperationType(StrEnum):
    """Defines how a new body from a body-creating feature should be merged with other bodies in the context.
    
    Documentation: <https://cad.onshape.com/FsDoc/library.html#NewBodyOperationType>
    """
    NEW = "NEW"
    ADD = "ADD"
    REMOVE = "REMOVE"
    INTERSECT = "INTERSECT"