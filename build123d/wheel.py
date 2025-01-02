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
LEFT_PADDING_WIDTH = 2.5

RIGHT_HOLE_RADIUS = 1.5
RIGHT_HOLE_RADIUS_TOLERANCE = 0.15
RIGHT_HOLE_DEPTH = 4.5

LEFT_HOLE_WIDTH = 9
LEFT_HOLE_UNDER_WIDTH = 5.5
LEFT_HOLE_DEPTH = WHEEL_WIDTH - RIGHT_HOLE_DEPTH
LEFT_HOLE_CHAMFER = 0.5

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

    # Right hole.
    with BuildSketch():
        Circle(RIGHT_HOLE_RADIUS + RIGHT_HOLE_RADIUS_TOLERANCE)
    extrude(amount=RIGHT_HOLE_DEPTH, mode=Mode.SUBTRACT)

    # Left hole.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)):
        with Locations(Rotation(0, 0, 45)):
            Rectangle(LEFT_HOLE_WIDTH, LEFT_HOLE_WIDTH)
        split(bisect_by=Plane.XZ.offset(HEX_DIAMETER_SHORT/2), keep=Keep.BOTTOM)
        with Locations(Rotation(0, 0, 45)):
            Rectangle(LEFT_HOLE_UNDER_WIDTH, LEFT_HOLE_UNDER_WIDTH)
    extrude(amount=-LEFT_HOLE_DEPTH, mode=Mode.SUBTRACT)


if __name__ == '__main__':
    from common.vscode import show_object
    from wheel_holder import holder
    from wheel_core import core
    show_object(wheel, name='Wheel')
    show_object(support, name='Support')
    show_object(core, name='Core')
    # export_stl(wheel.part, 'stl/test_wheel.stl')
    # export_stl(support.part, 'stl/test_support.stl')
    # export_stl(core.part, 'stl/test_core.stl')
