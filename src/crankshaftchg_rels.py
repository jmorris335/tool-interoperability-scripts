import numpy as np
import crankshaftchg_objects as obj
from onshape_api.client import Client

def Rget_pin_center_x(angle: float, offset: float, center_x: float, *args, **kwargs):
    '''Calculates the horizontal center of the crank pin based on the orientation of the pin when the first piston
    is TDC.'''
    pin_x = -offset * np.sin(angle) + center_x
    return pin_x

def Rget_pin_center_y(angle: float, offset: float, center_y: float, *args, **kwargs):
    '''Calculates the vertical center of the crank pin based on the orientation of the pin when the first piston
    is TDC.'''
    pin_y = offset * np.cos(angle) + center_y
    return pin_y

def Radd_feature_and_get_id(call: str, did: str, wid: str, eid: str, client: Client, *args, **kwargs):
    '''Adds a new feature (specified by the call) to the Onshape document.'''
    response = client.add_feature(did, wid, eid, call)
    id = response.json()['feature']['featureId']
    return id

def Rget_plane_id(face_id: str, did: str, wid: str, eid: str, client: Client, *args, **kwargs):
    """Returns the deterministic ID for the plane extracted from a feature."""
    query = f'qCreatedBy(makeId("{face_id}"), EntityType.FACE)'
    query_script = f'function(context is Context, queries) {{ return transientQueriesToStrings(evaluateQuery(context, {query})); }}'
    response = client.execute_feature_script(did, wid, eid, query_script)
    plane_id = response.json()['result']['message']['value'][-1]['message']['value']
    return plane_id

def Rget_mass(part_id: str, did: str, wid: str, eid: str, client: Client, *args, **kwargs):
    """Returns the mass of the part."""
    response = client.get_mass_properties(did, wid, eid, part_id)
    mass = response.json()['bodies']['additionalProp1']['mass'][0]
    return mass

def Rget_moment_of_inertia(axis: str, part_id: str, did: str, wid: str, eid: str, client: Client, *args, **kwargs):
    """Returns the moment of inertia around the principle axis (`x`, `y`, or `z`)"""
    response = client.get_mass_properties(did, wid, eid, part_id)
    moi = response.json()['bodies']['additionalProp1']['principalAxes'][0][axis]
    return moi 