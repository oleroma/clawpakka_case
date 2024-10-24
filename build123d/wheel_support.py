from build123d import *

from wheel import RIGHT_HOLE_RADIUS as AXLE_RADIUS
AXLE_X_OFFSET = 0.5
AXLE_Y_OFFSET = 11

BODY_X_LEN = 18
BODY_Z_LEN = 9.1
BODY_Z_ORIGIN = -3.6
BODY_X_TOLERANCE = 0.1

ANCHORS_X_LEN = 1.6
ANCHORS_Y_LEN = 2
ANCHORS_X_GAP = 13

with BuildPart() as support:
    # Translated plane by X offset.
    workplane = Plane(origin=(AXLE_X_OFFSET, 0))

    # Anchors.
    with BuildSketch(workplane.offset(0.5)):
        with Locations((ANCHORS_X_GAP/2, -AXLE_Y_OFFSET + BODY_X_TOLERANCE)):
            Rectangle(
                ANCHORS_X_LEN,
                ANCHORS_Y_LEN,
                align=(Align.MAX, Align.MAX),
            )
    extrude(amount=5)
    hang_edge = edges().filter_by(Axis.X)[0]
    chamfer(hang_edge, ANCHORS_Y_LEN-0.01)
    mirror(about=Plane.YZ.offset(AXLE_X_OFFSET))

    # Body.
    with BuildSketch(workplane.offset(BODY_Z_ORIGIN)):
        with Locations((0, -AXLE_Y_OFFSET + BODY_X_TOLERANCE)):
            Rectangle(
                BODY_X_LEN,
                AXLE_Y_OFFSET + AXLE_RADIUS - BODY_X_TOLERANCE,
                align=(Align.CENTER, Align.MIN),
            )
        # Thumbstick block cutout.
        with Locations((0, -5.5)):
            Rectangle(9.8, 11, mode=Mode.SUBTRACT)
    extrude(amount=BODY_Z_LEN)
    edge = edges().filter_by(Axis.X).sort_by(Axis.Z)[1]
    chamfer(edge, 2.6, angle=33)

    # Body remove big cylinder.
    with BuildSketch(Plane.XY.offset(-0.5)):
        Circle(11.5)
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Separator.
    with BuildSketch():
        with Locations((0, AXLE_RADIUS)):
            Rectangle(13, 6, align=(Align.CENTER, Align.MAX))
    extrude(amount=-0.5)

    # Cylinder.
    with BuildSketch():
        Circle(AXLE_RADIUS)
    extrude(amount=4)

if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(wheel)
    show_object(support)
    # wheel.part.export_stl('build123d/wheel_a1.stl')
    # support.part.export_stl('build123d/support_a1.stl')
