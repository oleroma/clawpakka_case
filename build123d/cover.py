from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Location, Locations,
    Axis, Rot,
    mirror, make_face, extrude, fillet, chamfer
    )

from ocp_vscode import show_object


COVER_WIDTH = 62
COVER_DEPTH = 37
COVER_HEIGHT = 2

POLY_WIDTH = 25
FILLET_SIZE = 2

USE_TABS = True ## False

with BuildPart() as cover:
    Box(COVER_WIDTH, COVER_DEPTH, COVER_HEIGHT)

    BOX_WIDTH = 6
    with Locations(
        (-COVER_WIDTH / 2 + 8 + BOX_WIDTH / 2, -COVER_DEPTH / 2 - BOX_WIDTH / 2, 3),
        (COVER_WIDTH / 2 - 8 - BOX_WIDTH / 2, -COVER_DEPTH / 2 - BOX_WIDTH / 2, 3)):
        Box(BOX_WIDTH, 6, 8)

    plane = Plane.XZ.offset(-COVER_DEPTH / 2)
    with BuildSketch(plane) as poly_sk:
        with BuildLine(Location((COVER_WIDTH / 2 - POLY_WIDTH, 1))) as line:
            Polyline((0, 0), (POLY_WIDTH, 0), (20, 5), (5, 5), (0, 0))
        make_face()
    extrude(amount=COVER_HEIGHT)
    mirror(about=Plane.YZ)

    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[2][0:2]
    fillet(edges, FILLET_SIZE)
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[1][1]
    fillet(edges, FILLET_SIZE)
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[1][2]
    fillet(edges, FILLET_SIZE)

    if USE_TABS:
        with Locations(
            (COVER_WIDTH / 2 - 8 - BOX_WIDTH, -COVER_DEPTH / 2 - 3, COVER_HEIGHT),
            (-COVER_WIDTH / 2 + 8, -COVER_DEPTH / 2 - 3, COVER_HEIGHT)):
            Box(0.2, 4, 2, rotation=(0, 5, 0))
        with Locations(
            (COVER_WIDTH / 2 - 8, -COVER_DEPTH / 2 - 3, COVER_HEIGHT),
            (-COVER_WIDTH / 2 + 8 + BOX_WIDTH, -COVER_DEPTH / 2 - 3, COVER_HEIGHT)):
            Box(0.2, 4, 2, rotation=(0, -5, 0))
        with Locations(
            (COVER_WIDTH / 2 - POLY_WIDTH / 2, COVER_DEPTH / 2, COVER_HEIGHT),
            (-COVER_WIDTH / 2 + POLY_WIDTH / 2, COVER_DEPTH / 2, COVER_HEIGHT)):
            Box(4, 0.2, 2, rotation=(5, 0, 0))


if __name__ in ['__main__', 'temp']:
    show_object(cover)
