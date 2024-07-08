from build123d import (
    BuildPart, BuildSketch, extrude, Rectangle, Circle, Mode, Plane, loft, Axis, chamfer)

from ocp_vscode import show_object

LOWER_BUTTON_HEIGHT = 2.4
LOWER_BUTTON_RAD = 5.8
LOWER_BUTTON_WIDTH = 9.6

TOP_BUTTON_HEIGHT = 13.9
MID_BUTTON_HEIGHT = 18.3 - TOP_BUTTON_HEIGHT - LOWER_BUTTON_HEIGHT
MID_BUTTON_RAD = 4.8

CHAMFER_SIZE = 0.5


with BuildPart() as button:
    with BuildSketch() as bottom_sk:
        Circle(LOWER_BUTTON_RAD)
        Rectangle(2 * LOWER_BUTTON_RAD, LOWER_BUTTON_WIDTH, mode=Mode.INTERSECT)
    
    with BuildSketch(Plane.XY.offset(LOWER_BUTTON_HEIGHT + MID_BUTTON_HEIGHT)) as top_sk:
        Circle(MID_BUTTON_RAD)

    loft()
    
    extrude(bottom_sk.sketch, amount=-LOWER_BUTTON_HEIGHT)
    extrude(top_sk.sketch, amount=TOP_BUTTON_HEIGHT)

    edges = button.part.edges().group_by(Axis.Z)[-1]
    chamfer(edges, CHAMFER_SIZE)

if __name__ in ['__main__', 'temp']:
    show_object(button)
