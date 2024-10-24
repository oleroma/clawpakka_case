from build123d import *
from math import cos, pi

WHEEL_INDENTS = 24
WHEEL_RADIUS_OUTER = 10.75
WHEEL_RADIUS_INNER = 10.25
WHEEL_WIDTH = 6.75
WHEEL_CHAMFER = 0.75

HEX_DIAMETER = 2  # Previously 2.05
HEX_DIAMETER_SHORT = HEX_DIAMETER * cos(pi / 6)

LEFT_PADDING_RADIUS = 3.5
LEFT_PADDING_WIDTH = 2.7
LEFT_HOLE_TOLERANCE = 0.1
LEFT_HOLE_RADIUS = (HEX_DIAMETER_SHORT / 2) + LEFT_HOLE_TOLERANCE
LEFT_HOLE_DEPTH = LEFT_PADDING_WIDTH
LEFT_HOLE_CHAMFER = 0.5
RIGHT_HOLE_RADIUS = 2
RIGHT_HOLE_RADIUS_TOLERANCE = 0.15
RIGHT_HOLE_DEPTH = 5


with BuildPart() as wheel:
    with BuildSketch():
        # Create a single indent chevron.
        with BuildLine(mode=Mode.PRIVATE) as line:
            # Create indent line.
            a = (WHEEL_RADIUS_OUTER, 0)
            b = PolarLine(
                start=(0, 0),
                length=WHEEL_RADIUS_INNER,
                angle=(180 / WHEEL_INDENTS),
                mode=Mode.PRIVATE,
            ) @ 1  # Point from line workaround.
            Line(a, b)
            # Mirror line into a chevron.
            mirror(about=Plane.YZ)
        # Repeat chevrons around a circle.
        with PolarLocations(0, WHEEL_INDENTS):
            add(line.line)
        make_face()
    extrude(amount=WHEEL_WIDTH)

    # Wheel chamfer.
    side_edges = edges().filter_by(Axis.Z, reverse=True)
    chamfer(side_edges, WHEEL_CHAMFER)

    # Left padding.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)):
        Circle(LEFT_PADDING_RADIUS)
    extrude(amount=LEFT_PADDING_WIDTH)

    # Left hole.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH + LEFT_PADDING_WIDTH)):
        def RegularTriangle(radius):
            return RegularPolygon(radius, 3, major_radius=False)
        with Locations(Rotation(0, 0, -30)):
            RegularTriangle(LEFT_HOLE_RADIUS)
        # with Locations(Rotation(0, 0, 180)):
        #     RegularTriangle(LEFT_HOLE_RADIUS)
    extrude(amount=-LEFT_HOLE_DEPTH, mode=Mode.SUBTRACT)

    # Star chamfer.
    star_edges = (edges()
        .filter_by(Axis.Z, reverse=True)
        .filter_by_position(
            Axis.Z,
            minimum=WHEEL_WIDTH + LEFT_PADDING_WIDTH,
            maximum=WHEEL_WIDTH + LEFT_PADDING_WIDTH,
        )
        .sort_by()[1:]
    )
    chamfer(star_edges, LEFT_HOLE_CHAMFER)

    # Right hole
    with BuildSketch():
        Circle(RIGHT_HOLE_RADIUS + RIGHT_HOLE_RADIUS_TOLERANCE)
    extrude(amount=RIGHT_HOLE_DEPTH, mode=Mode.SUBTRACT)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel_support import support
    from wheel_passtru import passtru
    show_object(wheel)
    show_object(support)
    show_object(passtru)
    export_stl(wheel.part, 'stl/wheel_a1.stl')
    export_stl(support.part, 'stl/support_a1.stl')
    export_stl(passtru.part, 'stl/passtru_a1.stl')
