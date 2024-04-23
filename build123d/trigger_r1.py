from build123d import (
    add, Axis, BuildLine, BuildPart, BuildSketch, Circle, chamfer, edges,
    faces, extrude, make_face, Mode, Plane, Polyline
)

SHAFT_RADIUS = 3
SHAFT_TOLERANCE = 0.1
SHAFT_Z = 13

BRIDGE_Z = 9.4
BRIDGE_RELIEF_Z = 0.9  # Cut-out to avoid potential 3D-printed overhangs.
BRIDGE_CONTACT_TOLERANCE_Y = 0.3  # Contact with the button switch.

SLAB_X_0 = 11
SLAB_X_1 = 17
SLAB_X_2 = 24
SLAB_X_3 = 29.5
SLAB_Y_0 = 4
SLAB_Y_1 = 9
SLAB_Z = 13
SLAB_Z_MISALIGN = 0.3  # Error in the original design?
SLAB_CHAMFER = 0.5

TOLERANCE_X = 0.1  # Applied only to some parts of the bridge and slab.
TOLERANCE_Y = 0.1  # Applied only to some parts of the bridge and slab.
TOLERANCE_Z = 0.7  # Applied to the height of all parts.

BRIDGE_POINTS = [
    (0,                       0),
    (0,                       1 - TOLERANCE_Y),
    (SLAB_X_0 + TOLERANCE_X,  SLAB_Y_0 - TOLERANCE_Y),
    (SLAB_X_1,                SLAB_Y_0 - TOLERANCE_Y),
    (SLAB_X_1,                2),
    (13.5,                    -2 + BRIDGE_CONTACT_TOLERANCE_Y),
    (8,                       -2 + BRIDGE_CONTACT_TOLERANCE_Y),
    (6,                       -3 + TOLERANCE_Y),
    (0,                       -3 + TOLERANCE_Y),
    (0,                       0),
]

RELIEF_POINTS = [
    (6,         -3),
    (6,         -2),
    (8,         -1),
    (SLAB_X_1,   0),
    (SLAB_X_1,  -3),
    (6,         -3)
]

SLAB_XY_POINTS = [
    (SLAB_X_0 + TOLERANCE_X,  SLAB_Y_0 - TOLERANCE_Y),
    (SLAB_X_0 + TOLERANCE_X,  SLAB_Y_1),
    (SLAB_X_3 - TOLERANCE_X,  SLAB_Y_1),
    (SLAB_X_3 - TOLERANCE_X,  5),
    (SLAB_X_2,                3.5),
    (SLAB_X_1,                3.5),
    (SLAB_X_0 + TOLERANCE_X,  SLAB_Y_0 - TOLERANCE_Y),
]

SLAB_XZ_POINTS = [
    (SLAB_XY_POINTS[0][0],  0),
    (SLAB_XY_POINTS[1][0],  BRIDGE_Z - TOLERANCE_Z),
    (SLAB_XY_POINTS[5][0],  SLAB_Z - TOLERANCE_Z),
    (SLAB_XY_POINTS[4][0],  SLAB_Z - TOLERANCE_Z),
    (SLAB_XY_POINTS[2][0],  BRIDGE_Z - TOLERANCE_Z + SLAB_Z_MISALIGN),
    (SLAB_XY_POINTS[3][0],  0),
    (SLAB_XY_POINTS[0][0],  0),
]

with BuildPart() as internal:
    # Shaft.
    with BuildSketch():
        Circle(SHAFT_RADIUS - SHAFT_TOLERANCE)
    extrude(amount=SHAFT_Z - TOLERANCE_Z)
    # Bridge.
    with BuildSketch():
        with BuildLine():
            Polyline(BRIDGE_POINTS)
        make_face()
    extrude(amount=BRIDGE_Z - TOLERANCE_Z)
    # Relief.
    plane = Plane.XY.offset(BRIDGE_Z - TOLERANCE_Z - BRIDGE_RELIEF_Z)
    with BuildSketch(plane):
        with BuildLine():
            Polyline(RELIEF_POINTS)
        make_face()
    extrude(amount=BRIDGE_RELIEF_Z, mode=Mode.SUBTRACT)

with BuildPart() as slab:
    # Slab XY.
    with BuildSketch():
        with BuildLine():
            Polyline(SLAB_XY_POINTS)
        make_face()
    extrude(amount=SLAB_Z - TOLERANCE_Z)
    # Slab XZ (intersects with XY).
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline(SLAB_XZ_POINTS)
        make_face()
    until = max([y for (x,y) in SLAB_XY_POINTS])  # Further away point in XY.sketch.
    extrude(amount=-until, mode=Mode.INTERSECT)
    # Chamfer.
    edges1 = faces().filter_by(Plane.XZ)[1].edges()  # Touchy face.
    edges2 = faces().filter_by(Plane.XY)[0].edges().filter_by(Axis.Y)  # Bottom edges.
    chamfer(edges1 + edges2, SLAB_CHAMFER)

# Combine both parts.
with BuildPart() as trigger_r1:
    add(internal.part)
    add(slab.part)

if __name__ in ['__main__', 'temp']:
    show_object(trigger_r1)
