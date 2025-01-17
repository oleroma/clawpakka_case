from build123d import (
    BuildPart, BuildSketch, BuildLine, Polyline, Plane, Rectangle, Location,
    Locations, Mode, Axis, Cylinder, Line, JernArc, RadiusArc, Spline, Circle, Transition, Box, Align,
    Until,
    extrude, mirror, make_face, loft, export_stl, offset, vertices, fillet, sweep
)

from ocp_vscode import set_defaults, Camera, show_object

from math import sin, radians

WALL_THICKNESS_AROUND = 1.2
WALL_THICKNESS_END = 0.5

PCB_WIDTH = 21.8
PCB_DEPTH = 46.9
DONGLE_HEIGHT = 4.12 # @ button
PCB_THICKNESS = 1.65

TOLERANCE_WIDTH = +0.35
TOLERANCE_DEPTH = +0.1
TOLERANCE_HEIGHT = +0.1

ANTENNA_WIDTH = 13.2 + 0.75 # measured + tolerance
ANTENNA_THICKNESS = 0.8 + 0.2
ANTENNA_DEPTH = 5.2 + 0.1


INSET = DONGLE_HEIGHT - PCB_THICKNESS

MAIN_PTS_OUTER = ((0, 0),
    (PCB_WIDTH / 2 + TOLERANCE_WIDTH + WALL_THICKNESS_AROUND, 0),
    (PCB_WIDTH / 2 + TOLERANCE_WIDTH + WALL_THICKNESS_AROUND, WALL_THICKNESS_AROUND + PCB_THICKNESS + 2 * TOLERANCE_HEIGHT),
    (PCB_WIDTH / 2 + TOLERANCE_WIDTH - INSET, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT + 2 * WALL_THICKNESS_AROUND),
    (0, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT + 2 * WALL_THICKNESS_AROUND))

# Not symetric due to button => Need to specify all points
MAIN_PTS_INNER = ((-PCB_WIDTH / 2 - TOLERANCE_WIDTH, WALL_THICKNESS_AROUND),
    (PCB_WIDTH / 2 + TOLERANCE_WIDTH, WALL_THICKNESS_AROUND),
    (PCB_WIDTH / 2 + TOLERANCE_WIDTH, PCB_THICKNESS + WALL_THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (PCB_WIDTH / 2 - INSET / 2 + TOLERANCE_WIDTH, DONGLE_HEIGHT + WALL_THICKNESS_AROUND - INSET / 2 + 2 * TOLERANCE_HEIGHT),
    (PCB_WIDTH / 2 - INSET * 1.5, DONGLE_HEIGHT + WALL_THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + INSET, DONGLE_HEIGHT + WALL_THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH / 2 - TOLERANCE_WIDTH, PCB_THICKNESS + WALL_THICKNESS_AROUND + 2 * TOLERANCE_HEIGHT),
    (-PCB_WIDTH / 2 - TOLERANCE_WIDTH, WALL_THICKNESS_AROUND - TOLERANCE_HEIGHT))


BUTTON_INSET_USB = 11.2 # inset from the USB
BUTTON_WIDTH = 3.2
BUTTON_INSET_PCB = 1.5 # inset from the edge of the PCB
BUTTON_DEPTH = 4.2

BUTTON_CUT_WIDTH = 0.3 #0.25
BUTTON_CUT_DEPTH = WALL_THICKNESS_AROUND - 0.2

EJECTION_HOLE_SIZE = 2.3 # slightly larger than hex-key

BUMP_WIDTH = 4


with BuildPart() as dongle_case:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline(MAIN_PTS_OUTER)
            mirror(about=Plane.YZ)
        make_face()

    extrude(amount=PCB_DEPTH)

    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline(MAIN_PTS_INNER)
        make_face()
    extrude(amount=PCB_DEPTH, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ.offset(PCB_DEPTH)):
        with BuildLine():
            Polyline(MAIN_PTS_OUTER)
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=ANTENNA_DEPTH)

    with BuildSketch(Plane.XZ.offset(PCB_DEPTH)):
        with Locations((0, WALL_THICKNESS_AROUND + DONGLE_HEIGHT / 2 + TOLERANCE_HEIGHT)):
            Rectangle(ANTENNA_WIDTH, DONGLE_HEIGHT + 2 * TOLERANCE_HEIGHT)
    extrude(amount=ANTENNA_DEPTH, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ.offset(PCB_DEPTH + ANTENNA_DEPTH)):
        with BuildLine():
            Polyline(MAIN_PTS_OUTER)
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=WALL_THICKNESS_END)

    with BuildSketch(Plane.XZ.offset(PCB_DEPTH)):
        with Locations((-ANTENNA_WIDTH / 2 - 1.5, WALL_THICKNESS_AROUND + EJECTION_HOLE_SIZE / 2 + 0.1),
                (ANTENNA_WIDTH / 2 + 1.5, WALL_THICKNESS_AROUND + EJECTION_HOLE_SIZE / 2 + 0.1)):
            Rectangle(EJECTION_HOLE_SIZE, EJECTION_HOLE_SIZE + 0.2)

    extrude(both=True, amount=-ANTENNA_DEPTH - WALL_THICKNESS_END, mode=Mode.SUBTRACT)

    with Locations((-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH / 2, -BUTTON_INSET_USB / 2 - 10, WALL_THICKNESS_AROUND / 2),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH / 2, 0, WALL_THICKNESS_AROUND / 2)):
        Box(BUTTON_CUT_WIDTH, BUTTON_INSET_USB + 20, WALL_THICKNESS_AROUND, mode=Mode.SUBTRACT)

    with Locations((-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH / 2 + BUMP_WIDTH / 2, -PCB_THICKNESS/2 - BUMP_WIDTH/2 + 1, WALL_THICKNESS_AROUND + PCB_THICKNESS / 4),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH / 2 - BUMP_WIDTH / 2, -PCB_THICKNESS/2 - BUMP_WIDTH/2 + 1, WALL_THICKNESS_AROUND + PCB_THICKNESS / 4)):
         Cylinder(PCB_THICKNESS / 2, BUMP_WIDTH - BUTTON_CUT_WIDTH, rotation=(0, 90, 90), arc_size=180)

    with BuildSketch(Plane.XZ.offset(BUMP_WIDTH/2 - 1)):
        with BuildLine():
            Polyline((PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH - PCB_THICKNESS / 2, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND))
        make_face()
    extrude(amount=PCB_THICKNESS, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ.offset(BUMP_WIDTH/2 - 1)):
        with BuildLine():
            Polyline((-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH + PCB_THICKNESS / 2, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUTTON_CUT_WIDTH, WALL_THICKNESS_AROUND))
        make_face()
    extrude(amount=PCB_THICKNESS, mode=Mode.SUBTRACT)


    with BuildSketch(Plane.XZ.offset(BUMP_WIDTH/2 - 1)):
        with BuildLine():
            Polyline((PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH, WALL_THICKNESS_AROUND),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH + PCB_THICKNESS / 2, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH, WALL_THICKNESS_AROUND))
        make_face()
    extrude(amount=PCB_THICKNESS, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XZ.offset(BUMP_WIDTH/2 - 1)):
        with BuildLine():
            Polyline(
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH, WALL_THICKNESS_AROUND),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH - PCB_THICKNESS / 2, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH, WALL_THICKNESS_AROUND + PCB_THICKNESS / 2),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH, WALL_THICKNESS_AROUND))
        make_face()
    extrude(amount=PCB_THICKNESS, mode=Mode.SUBTRACT)


    with BuildSketch(Plane.XY.offset(WALL_THICKNESS_AROUND)):
        with BuildLine():
            Polyline(
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH - PCB_THICKNESS, -BUMP_WIDTH/2 - 0.7),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH, -BUMP_WIDTH/2 - 0.7),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH, -BUMP_WIDTH/2 - 0.7 + PCB_THICKNESS),
            (-PCB_WIDTH / 2 - TOLERANCE_WIDTH + BUMP_WIDTH - PCB_THICKNESS, -BUMP_WIDTH/2 - 0.7))
        make_face()
    extrude(amount=PCB_THICKNESS / 2, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(WALL_THICKNESS_AROUND)):
        with BuildLine():
            Polyline(
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH + PCB_THICKNESS, -BUMP_WIDTH/2 - 0.7),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH, -BUMP_WIDTH/2 - 0.7),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH, -BUMP_WIDTH/2 - 0.7 + PCB_THICKNESS),
            (PCB_WIDTH / 2 + TOLERANCE_WIDTH - BUMP_WIDTH + PCB_THICKNESS, -BUMP_WIDTH/2 - 0.7))
        make_face()
    extrude(amount=PCB_THICKNESS / 2, mode=Mode.SUBTRACT)



# __main__ => show in VSCode
# temp     => show in CQEditor
if __name__ in ['__main__', 'temp']:
    if __name__ == '__main__':
        from ocp_vscode import show_object
        set_defaults(reset_camera=Camera.KEEP)
    show_object(dongle_case)

    print(f"Volume: {dongle_case.part.volume}")

##    export_stl(dongle_case.part, "dongle_case.stl")
