from build123d import *
from math import cos, pi

from wheel import HEX_DIAMETER, HEX_DIAMETER_SHORT
ENCODER_X_OFFSET = 14.5
HEX_LEN = 7.25
TAB_RADIUS = 6
TAB_WIDTH = 1


with BuildPart() as passtru:
    workplane = Plane.XY.offset(ENCODER_X_OFFSET)

    # Hex axle.
    with BuildSketch(workplane):
        RegularPolygon(HEX_DIAMETER / 2, 6)
    extrude(amount=-HEX_LEN)

    # Tab.
    with BuildSketch(workplane):
        printbed_offset = HEX_DIAMETER_SHORT / 2
        with Locations((0, -printbed_offset)):
            Circle(TAB_RADIUS)
            cutplane = Plane.XZ.offset(printbed_offset)
            split(bisect_by=cutplane, keep=Keep.BOTTOM)
    extrude(amount=TAB_WIDTH)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(wheel)
    show_object(passtru)
