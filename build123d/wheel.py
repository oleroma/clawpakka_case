from math import cos, pi
from build123d import (
    Axis, BuildLine, BuildPart, BuildSketch, Circle, Keep, Kind, Line,
    Location, Mode, Plane, PolarLine, PolarLocations, Polyline, RegularPolygon,
    add, chamfer, edges, extrude, make_face, mirror, offset, split
)

# Wheel
INDENTS = 24
WHEEL_RADIUS_OUTER = 10.75
WHEEL_RADIUS_INNER = 10.25
WHEEL_WIDTH = 6.75
CHAMFER = 0.75

# Core
CORE_RADIUS = 8
CORE_TOLERANCE = 0.1
RIGHT_CONTACT_LEN = 1.8
RIGHT_CONTACT_RADIUS = 2
HEX_DIAMETER = 2.05
HEX_LEN = 3.5
LEFT_AXLE_DIAMETER = HEX_DIAMETER * cos(pi / 6)
LEFT_AXLE_LEN = 5

# Holder
HOLDER_BASE_LEN = 13
HOLDER_TOP_LEN = 9.8
HOLDER_HEIGHT = 13
HOLDER_WIDTH = 8.3  # Original 7.
HOLDER_AXLE_TOLERANCE = 0.2
HOLDER_AXLE_OFFSET_FROM_TOP = 2

# Common.
CENTER = (0, 0)
PRINTBED_PLANE = Plane.XZ.offset(LEFT_AXLE_DIAMETER / 2)

# Core sketch.
with BuildSketch() as core_sketch:
    Circle(CORE_RADIUS)
    split(bisect_by=PRINTBED_PLANE, keep=Keep.BOTTOM)

# Wheel part.
with BuildPart() as wheel:
    with BuildSketch() as s:
        # Create a single indent chevron.
        with BuildLine(mode=Mode.PRIVATE) as l:
            # Create indent line.
            angle = 180 / INDENTS
            a = (WHEEL_RADIUS_OUTER, 0)
            b = PolarLine(CENTER, WHEEL_RADIUS_INNER, angle, mode=Mode.PRIVATE) @ 1
            Line(a, b)
            # Mirror line into a chevron.
            mirror(about=Plane.XZ)
        # Repeat chevrons around a circle.
        with PolarLocations(0, INDENTS):
            add(l.line)
        make_face()
    # Make 3D.
    extrude(amount=WHEEL_WIDTH)
    # Chamfer.
    edge_list = edges().filter_by(Axis.Z, reverse=True)
    chamfer(edge_list, CHAMFER)
    # Remove the core.
    with BuildSketch() as s:
        add(core_sketch.sketch)
        offset(amount=CORE_TOLERANCE, kind=Kind.INTERSECTION)
    extrude(amount=WHEEL_WIDTH, mode=Mode.SUBTRACT)

# Core part.
with BuildPart() as core:
    # Main core.
    add(core_sketch.sketch)
    extrude(amount=WHEEL_WIDTH)
    # Right contact.
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH)) as s:
        Circle(RIGHT_CONTACT_RADIUS)
        split(bisect_by=PRINTBED_PLANE, keep=Keep.BOTTOM)
    extrude(amount=RIGHT_CONTACT_LEN)
    # Right axle (hexagon).
    with BuildSketch(Plane.XY.offset(WHEEL_WIDTH + RIGHT_CONTACT_LEN)) as s:
        RegularPolygon(HEX_DIAMETER / 2, 6)
    extrude(amount=HEX_LEN)
    # Left axle.
    with BuildSketch() as s:
        Circle(LEFT_AXLE_DIAMETER / 2)
    # Make 3D.
    extrude(amount=-LEFT_AXLE_LEN)

# Holder part.
with BuildPart() as holder:
    with BuildSketch(Plane.XY) as s:
        offset = Location((0, HOLDER_AXLE_OFFSET_FROM_TOP))
        with BuildLine(offset) as l:
            # Create half polygon.
            Polyline([
                CENTER,
                (HOLDER_TOP_LEN / 2, 0),
                (HOLDER_BASE_LEN / 2, -HOLDER_HEIGHT),
                (0, -HOLDER_HEIGHT),
            ])
            # Mirror into full polygon.
            mirror(l.line, about=Plane.YZ)
        make_face()
        # Remove hole.
        radius = (LEFT_AXLE_DIAMETER / 2) + HOLDER_AXLE_TOLERANCE
        Circle(radius, mode=Mode.SUBTRACT)
    # Make 3D.
    extrude(amount=-HOLDER_WIDTH)


if __name__ in ['__main__', 'temp']:
    show_object(wheel)
    show_object(core)
    show_object(holder)
