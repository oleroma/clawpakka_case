from build123d import *

NECK_HEIGHT = 8.5
NECK_RADIUS = 2.5

HEAD_RADIUS = 4
HEAD_TALL = 2
HEAD_CHAMFER = 0.5

DOME_RADIUS = 12
DOME_CUT = DOME_RADIUS - 1.75

HOLE_TOLERANCE = 0.12
HOLE_RADIUS = 2 + HOLE_TOLERANCE
HOLE_CUT = 1.5 + HOLE_TOLERANCE
HOLE_DEPTH = 5 + 0.5


with BuildPart() as thumbstick:
    # Dome.
    with BuildSketch(Plane.XZ) as dome_external:
        Circle(radius=DOME_RADIUS)
        split(bisect_by=Plane.XZ.offset(-DOME_CUT), keep=Keep.BOTTOM)
        split(bisect_by=Plane.YZ)

    # Shaft and head.
    with BuildSketch(Plane.XZ) as shaft:
        with Locations((0, DOME_CUT)):
            Rectangle(NECK_RADIUS, NECK_HEIGHT, align=Align.MIN)
            with BuildLine(Location((0, DOME_CUT))) as head:
                Polyline(
                    (0,           NECK_HEIGHT),
                    (HEAD_RADIUS, NECK_HEIGHT),
                    (HEAD_RADIUS, NECK_HEIGHT - HEAD_TALL),
                    (0,           NECK_HEIGHT - HEAD_TALL - HEAD_RADIUS),
                )
            make_face()

    # Make 3D.
    revolve(axis=Axis.Z)

    # Remove hole.
    with BuildSketch(Plane.XY.offset(DOME_CUT)) as hole:
        Circle(radius=HOLE_RADIUS)
        Rectangle(HOLE_RADIUS * 2, HOLE_CUT * 2, mode=Mode.INTERSECT)
    extrude(amount=HOLE_DEPTH, mode=Mode.SUBTRACT)

    # Chamfer top edge.
    top_edge = edges().sort_by(Axis.Z)[-1]
    chamfer(top_edge, HEAD_CHAMFER)


if __name__ == '__main__':
    from common.vscode import show_object
    show_object(thumbstick, name='Thumbstick')
    # export_stl(thumbstick.part, 'stl/test_thumbstick_right.stl')
