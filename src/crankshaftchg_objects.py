from constrainthg import Node
from onshape_api.library import *
from onshape_api.client import Client, DocumentIDs
import json

class CircleEntity:
    def __init__(self, name: str, **kwargs):
        self.name = Node(f'name for {name}', name)
        self.radius = Node(f'radius for {name}', kwargs.get('radius', None))
        self.xCenter = Node(f'xCenter for {name}', kwargs.get('xCenter', None))
        self.yCenter = Node(f'yCenter for {name}', kwargs.get('yCenter', None))
        self.call = Node(f'call for {name}', kwargs.get('call', None))

    @staticmethod
    def Rget_call(radius, xCenter, yCenter, *args, **kwargs):
        '''An internal relationship that never changes.'''
        out = {
            "btType": "BTMSketchCurve-4",
            "geometry": {
                "btType": "BTCurveGeometryCircle-115",
                "radius": radius,  
                "xCenter": xCenter,
                "yCenter": yCenter,  
                "xDir": 1,
                "yDir": 0, 
                "clockwise": False, 
            },
            "centerId": "circle-entity.center",
            "entityId": "circle-entity"
        }
        return out

class CircleSketch:
    def __init__(self, name: str, **kwargs):
        self.name = Node(f'Name for {name}', name)
        self.id = Node(f'ID for {name}')
        self.plane_id = Node(f'Deterministic id of plane for {name}', kwargs.get('plane', None))
        self.call = Node(f'Call for {name}', kwargs.get('call', None))

    @staticmethod
    def Rget_call(name, plane_id, circle_call: str, *args, **kwargs):
        out = {
            "btType": "BTFeatureDefinitionCall-1406",
            "feature" : {
                "btType": "BTMSketch-151", 
                "featureType": "newSketch", 
                "name": name,
                "parameters" : [
                    {
                    "btType": "BTMParameterQueryList-148",
                    "queries": [
                        {
                        "btType": "BTMIndividualQuery-138",
                        "deterministicIds": [plane_id]
                        }
                    ],
                    "parameterId": "sketchPlane", 
                    }
                ]
            }
        }
        out["feature"]["entities"] = [circle_call]
        out["feature"]["constraints"] = list() 
        return out

class Cylinder:
    def __init__(self, name: str, **kwargs):
        self.name = Node(f'Name for {name}', name)
        self.id = Node(f'ID for {name}')
        self.operationType = Node(f'OperationType for {name}', kwargs.get('operation_type', SMNewBodyOperationType.NEW))
        self.endBound = Node(f'endBound for {name}', SMExtrudeBoundingTypes.BLIND)
        self.depth = Node(f'depth of {name}', kwargs.get('depth', None))
        self.call = Node(f'Call for {name}', kwargs.get('call', None))

    @staticmethod
    def Rget_extrusion_call(name: str, feature_id: str, depth: float, endBound: SMExtrudeBoundingTypes, operationType: SMNewBodyOperationType, *args, **kwargs):
        """Makes the JSON output for a extrude of the feature specified as the id."""
        defaults = dict(
            body_type = "SOLID",
            units = "mm"        
        )
        kwargs = defaults | kwargs

        params = [
            dict(
                btType = "BTMParameterEnum-145",
                value = kwargs['body_type'],
                enumName = "ExtendedToolBodyType",
                parameterId = "bodyType",
            ), dict(
                btType = "BTMParameterEnum-145",
                value = operationType,
                enumName = "NewBodyOperationType",
                parameterId = "operationType",
            ), dict(
                btType = "BTMParameterQueryList-148",
                queries = [{
                    "btType": "BTMIndividualSketchRegionQuery-140",
                    "featureId": feature_id
                    }],
                parameterId = "entities",
            ), dict(
                btType = "BTMParameterEnum-145",
                value = str(endBound),
                enumName = "BoundingType",
                parameterId = "endBound",
            ), dict(
                btType = "BTMParameterQuantity-147",
                expression = f"{depth} {kwargs['units']}",
                parameterId = "depth",
            )]
        feature = dict(
            btType = "BTMFeature-134",
            featureType = "extrude",
            name = name,
            parameters = params,
            returnAfterSubfeatures = False,
            suppressed = False,
        )
        out = dict(
            btType = "BTFeatureDefinitionCall-1406",
            feature = feature,
        )
        return json.dumps(out)
