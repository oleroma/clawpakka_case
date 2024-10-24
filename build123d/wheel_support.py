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

    # Body.
    with BuildSketch(workplane.offset(BODY_Z_ORIGIN)):
        with Locations((0, -AXLE_Y_OFFSET + BODY_X_TOLERANCE)):
            Rectangle(
                BODY_X_LEN,
                AXLE_Y_OFFSET + AXLE_RADIUS - BODY_X_TOLERANCE,
                align=(Align.CENTER, Align.MIN),
            )
    extrude(amount=BODY_Z_LEN)
    edge = (edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[0]
        .sort_by(Axis.Y, reverse=True)[0]
    )
    chamfer(edge, length=2.9, length2=1.8)

    # Anchors.
    with BuildSketch(workplane.offset(0.5)):
        with Locations((0, -AXLE_Y_OFFSET + BODY_X_TOLERANCE)):
            Rectangle(
                ANCHORS_X_GAP,
                ANCHORS_Y_LEN,
                align=(Align.CENTER, Align.MAX),
            )
    extrude(amount=5)
    hang_edge = (edges()
        .filter_by(Axis.X)
        .group_by(Axis.Y)[0]
        .sort_by(Axis.Z)[0]
    )
    chamfer(hang_edge, ANCHORS_Y_LEN-0.01)

    # Remove thumbstick block.
    with BuildSketch(workplane.offset(BODY_Z_ORIGIN)):
        Rectangle(9.8, 20, align=(Align.CENTER, Align.MAX))
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Remove big cylinder (aligned with wheel).
    with BuildSketch(Plane.XY.offset(-0.5)):
        Circle(11.5)
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Plate.
    with BuildSketch():
        with Locations((0, AXLE_RADIUS)):
            Rectangle(13, 6, align=(Align.CENTER, Align.MAX))
    extrude(amount=-0.5)

    # Axle.
    with BuildSketch():
        Circle(AXLE_RADIUS)
    extrude(amount=4)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(wheel)
    show_object(support)
