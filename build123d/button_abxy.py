from build123d import (
    BuildPart, BuildSketch, Rectangle, Circle, Mode, Plane, Axis, Location, Compound,
    chamfer, extrude, loft
    )

try:
    from ocp_vscode import show_object
except ModuleNotFoundError:
    pass

LOWER_BUTTON_HEIGHT = 2.4
LOWER_BUTTON_RAD = 5.8
LOWER_BUTTON_WIDTH = 9.6

TOP_BUTTON_HEIGHT = 13.9
MID_BUTTON_HEIGHT = 18.3 - TOP_BUTTON_HEIGHT - LOWER_BUTTON_HEIGHT
MID_BUTTON_RAD = 4.8

CHAMFER_SIZE = 0.5

BUTTON_OFFSET = 12


with BuildPart() as button_abxy:
    with BuildSketch() as bottom_sk:
        Circle(LOWER_BUTTON_RAD)
        Rectangle(2 * LOWER_BUTTON_RAD, LOWER_BUTTON_WIDTH, mode=Mode.INTERSECT)
    
    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT + MID_BUTTON_HEIGHT)) as top_sk:
        Circle(MID_BUTTON_RAD)

    loft()
    
    extrude(bottom_sk.sketch, amount=-LOWER_BUTTON_HEIGHT)
    extrude(top_sk.sketch, amount=TOP_BUTTON_HEIGHT)

    edges = button_abxy.part.edges().group_by(Axis.Z)[-1]
    chamfer(edges, CHAMFER_SIZE)

    button_abxy_2 = button_abxy.part.mirror(Plane.YZ.offset(BUTTON_OFFSET))
    button_abxy_3 = button_abxy.part.rotate(angle=90, axis=Axis.Z).move(loc=Location((BUTTON_OFFSET, BUTTON_OFFSET, 0)))
    button_abxy_4 = button_abxy.part.rotate(angle=90, axis=Axis.Z).move(loc=Location((BUTTON_OFFSET, -BUTTON_OFFSET, 0)))

button_abxy_assembly = Compound(children=button_abxy, button_abxy_2, button_abxy_3, button_abxy_4)

if __name__ in ['__main__', 'temp']:
    show_object(button_abxy_assembly)


