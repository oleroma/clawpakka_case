from build123d import *

from wheel import RIGHT_HOLE_RADIUS as AXLE_RADIUS
AXLE_LEN = 1.5
AXLE_X_OFFSET = 0.5
AXLE_Y_OFFSET = 11

BODY_X_LEN = 18
BODY_Z_LEN = 3.5
BODY_Y_TOLERANCE = 0  # 0.4

SEPARATOR_Z_LEN = 0.5

BLOCK_X = 9.6  # 9.8
BLOCK_Y = 15
BLOCK_Y_OFFSET = 0.3  # 0.5

# Translated plane by X offset.
workplane = Plane(origin=(AXLE_X_OFFSET, 0))

with BuildPart() as support:
    # Body.
    with BuildSketch(workplane.offset(-SEPARATOR_Z_LEN)) as body_s:
        with Locations((0, -AXLE_Y_OFFSET + BODY_Y_TOLERANCE)):
            Rectangle(
                BODY_X_LEN,
                AXLE_Y_OFFSET + AXLE_RADIUS - BODY_Y_TOLERANCE,
                align=(Align.CENTER, Align.MIN),
            )
    extrude(amount=-BODY_Z_LEN)

    # Chamfer from bed.
    edge_bed = (edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[0]
        .sort_by(Axis.Y, reverse=True)[0]
    )
    chamfer(edge_bed, length=3.1, length2=0.8)

    # Fillet body corners
    edges_corner = (edges()
        .filter_by(Axis.Z)
        .group_by(Axis.Y, reverse=True)[0]
    )
    fillet(edges_corner, radius=4)

    # Remove thumbstick block.
    with BuildSketch(workplane.offset(-SEPARATOR_Z_LEN - BODY_Z_LEN)):
        with Locations((0, BLOCK_Y_OFFSET)):
            Rectangle(BLOCK_X, BLOCK_Y, align=(Align.CENTER, Align.MAX))
    extrude(amount=10, mode=Mode.SUBTRACT)

    # Separator.
    with BuildSketch(workplane) :
        with Locations((0, AXLE_RADIUS)):
            RectangleRounded(12.5, AXLE_RADIUS*2, radius=1, align=(Align.CENTER, Align.MAX))
    extrude(amount=-SEPARATOR_Z_LEN)

    # Axle.
    with BuildSketch():
        Circle(AXLE_RADIUS)
    extrude(amount=AXLE_LEN)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(support, name="Support")
    show_object(wheel, name="Wheel")
