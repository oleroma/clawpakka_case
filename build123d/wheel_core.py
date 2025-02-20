from build123d import *
from math import cos, pi

from wheel import (
    HEX_DIAMETER,
    HEX_DIAMETER_SHORT,
    WHEEL_WIDTH,
    LEFT_SLOT_WIDTH,
    LEFT_SLOT_DEPTH,
)

HEX_LEN = 8
SPACER_RADIUS = 2
SPACER_DEPTH = 1


with BuildPart() as core:
    # Hex axle.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)):
        RegularPolygon(HEX_DIAMETER / 2, 6)
    extrude(amount=HEX_LEN)

    # Body.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)):
        Circle(LEFT_SLOT_WIDTH / 2)
        cutplane = Plane.XZ.offset(HEX_DIAMETER_SHORT / 2)
        split(bisect_by=cutplane, keep=Keep.BOTTOM)
    extrude(amount=-LEFT_SLOT_DEPTH)

    # Spacer.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)):
        Circle(SPACER_RADIUS)
        cutplane = Plane.XZ.offset(HEX_DIAMETER_SHORT / 2)
        split(bisect_by=cutplane, keep=Keep.BOTTOM)
    extrude(amount=SPACER_DEPTH)

if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(core, name="Core")
    show_object(wheel, name="Wheel")
