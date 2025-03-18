from constrainthg import Node, Hypergraph
import constrainthg.relations as R
import crankshaftchg_objects as obj
from crankshaftchg_rels import *
from onshape_api.library import *
from onshape_api.client import Client, DocumentIDs
import onshape_relations as OnShapeR

# NODES
## Geometery
center_point_x = Node('center_point_x', 0.)
center_point_y = Node('center_point_y', 0.)
shaft_dia = Node('shaft_dia', .025)
pin_dia = Node('pin_dia', .020)
web_dia = Node('web_dia', .100)
bearing_length = Node('bearing_length', 25)
pin_length = Node('pin_length', 25)
web_length = Node('web_length', 10)
shaft_length = Node('shaft_length')
pin_offset = Node('pin_offset', .030)
num_pins = Node('number of pins', 4)
ORIENTATION = [Node(f'pin{i}_orientation', 0.7, description='angle to vertical of crank pin') for i in range(num_pins.static_value)]

## CAD Features
initial_plane = Node('Initial plane for modeling', 'Front')
ENTITY_BEARINGS = [obj.CircleEntity(f'Circle-Bearing_start')]
SKETCH_BEARINGS = [obj.CircleSketch(f'Sketch-Bearing_start')]
EXTRUDE_BEARINGS = [obj.Cylinder(f'Sketch-Extrude_start', operationType=SMNewBodyOperationType.NEW)]
ENTITY_WEB1S, ENTITY_PINS, ENTITY_WEB2S = [], [], []
SKETCH_WEB1S, SKETCH_PINS, SKETCH_WEB2S = [], [], []
EXTRUDE_WEB1S, EXTRUDE_PINS, EXTRUDE_WEB2S = [], [], []

for NAME in range(1, num_pins.static_value+1):
    ENTITY_BEARINGS.append(obj.CircleEntity(f'Circle-Bearing{NAME}'))
    ENTITY_WEB1S.append(obj.CircleEntity(f'Circle-Web{NAME}_1'))
    ENTITY_PINS.append(obj.CircleEntity(f'Circle-Pin{NAME}'))
    ENTITY_WEB2S.append(obj.CircleEntity(f'Circle-Web{NAME}_2'))
    SKETCH_BEARINGS.append(obj.CircleSketch(f'Sketch-Bearing{NAME}'))
    SKETCH_WEB1S.append(obj.CircleSketch(f'Sketch-Web{NAME}_1'))
    SKETCH_PINS.append(obj.CircleSketch(f'Sketch-Pin{NAME}'))
    SKETCH_WEB2S.append(obj.CircleSketch(f'Sketch-Web{NAME}_2'))
    EXTRUDE_BEARINGS.append(obj.Cylinder(f'Extrude-Bearing{NAME}', operationType=SMNewBodyOperationType.ADD))
    EXTRUDE_WEB1S.append(obj.Cylinder(f'Extrude-Web{NAME}_1', operationType=SMNewBodyOperationType.ADD))
    EXTRUDE_PINS.append(obj.Cylinder(f'Extrude-Pin{NAME}', operationType=SMNewBodyOperationType.ADD))
    EXTRUDE_WEB2S.append(obj.Cylinder(f'Extrude-Web{NAME}_2', operationType=SMNewBodyOperationType.ADD))

ENTITIES = ENTITY_BEARINGS + ENTITY_WEB1S + ENTITY_PINS + ENTITY_WEB2S
SKETCHES = SKETCH_BEARINGS + SKETCH_WEB1S + SKETCH_PINS + SKETCH_WEB2S
EXTRUDES = EXTRUDE_BEARINGS + EXTRUDE_WEB1S + EXTRUDE_PINS + EXTRUDE_WEB2S
SECTIONS = [(ENTITY_BEARINGS[0], SKETCH_BEARINGS[0], EXTRUDE_BEARINGS[0])]
for i in range(len(ENTITY_PINS)):
    SECTIONS.append((ENTITY_WEB1S[i], SKETCH_WEB1S[i], EXTRUDE_WEB1S[i]))
    SECTIONS.append((ENTITY_PINS[i], SKETCH_PINS[i], EXTRUDE_PINS[i]))
    SECTIONS.append((ENTITY_WEB2S[i], SKETCH_WEB2S[i], EXTRUDE_WEB2S[i]))
    SECTIONS.append((ENTITY_BEARINGS[i+1], SKETCH_BEARINGS[i+1], EXTRUDE_BEARINGS[i+1]))

## Onshape Connectivity
cred_filepath = Node('filepath for API credentials', './coding/SECRETS.json') #Change this to cred.json
client = Node('client for Onshape part studio')
did = Node('document id for part studio', '99ccbc50135e7bd6a47fc0fb')
wvm = Node('wvm for part studio', 'w')
wvmid = Node('workspace version number for part studio', '03b2576bbb9b2c4ef0de9bf4')
eid = Node('element id for part studio', 'c081126bd4e3181bb497cf01')

chg = Hypergraph()
chg.add_edge({'cred_path': cred_filepath}, client, lambda cred_path, **kw : Client(creds=cred_path, logging=False))

for entity in ENTITY_BEARINGS:
    chg.add_edge(shaft_dia, entity.radius, lambda s1, **kw : s1 / 2)
    chg.add_edge(center_point_x, entity.xCenter, R.Rfirst)
    chg.add_edge(center_point_y, entity.yCenter, R.Rfirst)

for entity in ENTITY_WEB1S + ENTITY_WEB2S:
    chg.add_edge(web_dia, entity.radius, lambda s1, **kw : s1 / 2)
    chg.add_edge(center_point_x, entity.xCenter, R.Rfirst)
    chg.add_edge(center_point_y, entity.yCenter, R.Rfirst)

for entity, orientation in zip(ENTITY_PINS, ORIENTATION):
    chg.add_edge(pin_dia, entity.radius, lambda s1, **kw : s1 / 2)
    chg.add_edge({'angle':orientation, 'offset':pin_offset, 'center_x': center_point_x}, 
                 entity.xCenter, Rget_pin_center_x)
    chg.add_edge({'angle':orientation, 'offset':pin_offset, 'center_y': center_point_y}, 
                 entity.yCenter, Rget_pin_center_y)
    
for extrude in EXTRUDE_BEARINGS:
    chg.add_edge(bearing_length, extrude.depth, R.Rfirst)

for extrude in EXTRUDE_WEB1S + EXTRUDE_WEB2S:
    chg.add_edge(web_length, extrude.depth, R.Rfirst)

for extrude in EXTRUDE_PINS:
    chg.add_edge(pin_length, extrude.depth, R.Rfirst)

for entity, sketch, extrude in SECTIONS:
    chg.add_edge({'radius': entity.radius, 'xCenter': entity.xCenter, 'yCenter':entity.yCenter},
                entity.call, obj.CircleEntity.Rget_call)
    if entity is ENTITIES[0]:
        chg.add_edge({'face_id': initial_plane, 'did': did, 'wid': wvmid, 'eid': eid, 'client': client}, 
                    sketch.plane_id, Rget_plane_id)
    else:
        prev_extrude = SECTIONS[SECTIONS.index((entity, sketch, extrude)) - 1][-1]
        chg.add_edge({'face_id': prev_extrude.id, 'did': did, 'wid': wvmid, 'eid': eid, 'client': client}, 
                    sketch.plane_id, Rget_plane_id)
    chg.add_edge({'name': sketch.name, 'plane_id': sketch.plane_id, 'circle_call': entity.call}, 
                 sketch.call, obj.CircleSketch.Rget_call)
    chg.add_edge({'call': sketch.call, 'did': did, 'wid': wvmid, 'eid': eid, 'client': client},
                 sketch.id, Radd_feature_and_get_id)
    chg.add_edge({'name': extrude.name, 'feature_id': sketch.id, 'depth': extrude.depth, 'endBound': extrude.endBound, 'operationType': extrude.operationType}, extrude.call, obj.Cylinder.Rget_extrusion_call)
    chg.add_edge({'call': extrude.call, 'did': did, 'wid': wvmid, 'eid': eid, 'client': client}, extrude.id, Radd_feature_and_get_id)
    
t, solved_values = chg.solve(EXTRUDES[-1].id)