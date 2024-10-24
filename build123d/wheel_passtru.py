from build123d import *
from math import cos, pi

HEX_DIAMETER = 2.05  # 2 millimeter + extra for better fit.
HEX_DIAMETER_SHORT = HEX_DIAMETER * cos(pi / 6)
HEX_LEN = 7.5

with BuildPart() as passtru:

    with BuildSketch(Plane.XY.offset(7.5)):
        RegularPolygon(HEX_DIAMETER / 2, 6)
    extrude(amount=HEX_LEN)

    with BuildSketch(Plane.XY.offset(7.5 + HEX_LEN)):
        with Locations((0, -HEX_DIAMETER_SHORT/2)):
            Circle(6)
            Rectangle(20, 20, align=(Align.CENTER, Align.MAX), mode=Mode.SUBTRACT)
    extrude(amount=1)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel import wheel
    show_object(wheel)
    show_object(passtru)
    # passtru.part.export_stl('build123d/passtru_a1.stl')
