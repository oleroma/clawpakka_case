from build123d import *

from wheel import RIGHT_HOLE_RADIUS as AXLE_RADIUS
AXLE_X_OFFSET = 0.5
AXLE_Y_OFFSET = 11

BODY_X_LEN = 18
BODY_Z_LEN = 9.1
BODY_Z_ORIGIN = -3.6
BODY_Y_TOLERANCE = 0.4

ANCHORS_X_LEN = 1.6
ANCHORS_Y_LEN = 2
ANCHORS_X_GAP = 13
ANCHORS_Z_ORIGIN = 0
ANCHORS_Z_LEN = 5.5


with BuildPart() as support:
    # Translated plane by X offset.
    workplane = Plane(origin=(AXLE_X_OFFSET, 0))

    # Body.
    with BuildSketch(workplane.offset(BODY_Z_ORIGIN)) as body:
        with Locations((0, -AXLE_Y_OFFSET + BODY_Y_TOLERANCE)):
            Rectangle(
                BODY_X_LEN,
                AXLE_Y_OFFSET + AXLE_RADIUS - BODY_Y_TOLERANCE,
                align=(Align.CENTER, Align.MIN),
            )
    extrude(amount=BODY_Z_LEN)

    # Fillet body corners
    corners = (edges()
        .filter_by(Axis.Z)
        .group_by(Axis.Y, reverse=True)[0]
    )
    fillet(corners, radius=4)

    # Chamfer from bed.
    bed_edge = (edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[0]
        .sort_by(Axis.Y, reverse=True)[0]
    )
    chamfer(bed_edge, length=1.3, length2=2.7)

    # Anchors.
    with BuildSketch(workplane.offset(ANCHORS_Z_ORIGIN)) as anchors:
        with Locations((0, -AXLE_Y_OFFSET + BODY_Y_TOLERANCE)):
            Rectangle(
                ANCHORS_X_GAP,
                ANCHORS_Y_LEN,
                align=(Align.CENTER, Align.MAX),
            )
    extrude(amount=ANCHORS_Z_LEN)
    hang_edge = (edges()
        .filter_by(Axis.X)
        .group_by(Axis.Y)[0]
        .sort_by(Axis.Z)[0]
    )
    chamfer(hang_edge, ANCHORS_Y_LEN-0.01)

    # Remove thumbstick block.
    with BuildSketch(workplane.offset(BODY_Z_ORIGIN)):
        with Locations((0, 0.5)):
            Rectangle(9.8, 20, align=(Align.CENTER, Align.MAX))
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Remove big cylinder (aligned with wheel).
    with BuildSketch(Plane.XY.offset(-0.5)):
        Circle(11.5)
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Plate.
    with BuildSketch(workplane):
        with Locations((0, AXLE_RADIUS)):
            RectangleRounded(12, 6, radius=1, align=(Align.CENTER, Align.MAX))
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
