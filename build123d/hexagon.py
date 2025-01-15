from build123d import (
    BuildPart, BuildSketch, BuildLine, Polyline, Circle, Plane, Locations, Mode, Location,
    mirror, make_face, extrude, add)

import math

try:
    from ocp_vscode import show_object
except ModuleNotFoundError:
    pass


# top hex
HEX_TOP_HEIGHT = 1.9
HEX_DEPTH = 40
HEX_PTS = ( ## only half => mirror
    (0, 0),
    (18, 10),
    (18, 30),
    (0, HEX_DEPTH))

HEX_HOLE_LOCATIONS=(
    (0, 8),
    (0, 32),
    (12, 20),
    (-12, 20))

hex_hole_radius=5


# trapezoid
TRAPEZ_WIDTH = 2.758 ## tight: 2.8
TRAPEZ_PTS = (
    (0, 0),
    (math.sqrt(10 * 10 + 10 * 10), 0), # diagonal of width (10) and depth (10)
    (3, 18 - HEX_TOP_HEIGHT),
    (0, 18 - HEX_TOP_HEIGHT))


with BuildPart() as chex:
    with BuildSketch():
        with BuildLine() as top_outline:
           line = Polyline(HEX_PTS)
           mirror(top_outline.line, about=Plane.YZ)
        make_face()

        with Locations(HEX_HOLE_LOCATIONS):
            Circle(hex_hole_radius, mode=Mode.SUBTRACT)

    extrude(amount=HEX_TOP_HEIGHT)

    with BuildPart(mode=Mode.PRIVATE) as bottom_pt:
        plane = Plane.XZ.offset(-TRAPEZ_WIDTH / 2)
        with BuildSketch(plane):
            with BuildLine() as bottom_outline:
                line = Polyline(TRAPEZ_PTS)
                mirror(bottom_outline.line, about=Plane.YZ)

            make_face()
        extrude(amount=TRAPEZ_WIDTH)

    with Locations(Location((0, HEX_DEPTH / 2, HEX_TOP_HEIGHT))):
        add(bottom_pt, rotation=(0, 0, -45))
        add(bottom_pt, rotation=(0, 0, 45))


if __name__ in ['__main__', 'temp']:
    show_object(chex)
    print(f"Volume: {chex.part.volume}")
