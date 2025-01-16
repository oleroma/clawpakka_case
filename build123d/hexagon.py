from build123d import *
import math

BASE_X_LEN = 36
BASE_Y_LEN = 40
BASE_Z_LEN = 1.9
BASE_Y_SIDE = 20

HOLE_RADIUS = 5
HOLE_DISTANCE_FROM_CENTER = 12

TABS_Z_LEN = 4

TRAPEZ_WIDTH = 2.758  ## Tight version was 2.8.
TRAPEZ_HEIGHT = 18
TRAPEZ_TIP_WIDTH = 2.2
TRAPEZ_PTS = (
    (0, 0),
    (math.sqrt(10**2 + 10**2),         0),  # Diagonal of 10x10 (Blender legacy).
    (TRAPEZ_TIP_WIDTH, TRAPEZ_HEIGHT - BASE_Z_LEN),
    (0,                TRAPEZ_HEIGHT - BASE_Z_LEN),
)

with BuildPart() as chex:
    # Base.
    with BuildSketch():
        with BuildLine():
            Polyline([
                (0,            BASE_Y_LEN/2),
                (BASE_X_LEN/2, BASE_Y_SIDE/2),
                (BASE_X_LEN/2, 0),
            ])
            mirror(about=Plane.YZ)
            mirror(about=Plane.XZ)
        make_face()
        # Holes.
        locations = [
            (0, HOLE_DISTANCE_FROM_CENTER),
            (0, -HOLE_DISTANCE_FROM_CENTER),
            (HOLE_DISTANCE_FROM_CENTER, 0),
            (-HOLE_DISTANCE_FROM_CENTER, 0),
        ]
        with Locations(locations):
            Circle(HOLE_RADIUS, mode=Mode.SUBTRACT)
    extrude(amount=BASE_Z_LEN)

    # Trapezoid.
    with BuildPart(mode=Mode.PRIVATE) as trapezoid_pt:
        plane = Plane.XZ.offset(-TRAPEZ_WIDTH / 2)
        with BuildSketch(plane):
            with BuildLine():
                Polyline(TRAPEZ_PTS)
                mirror(about=Plane.YZ)
            make_face()
        extrude(amount=TRAPEZ_WIDTH)
    with Locations((0, 0, BASE_Z_LEN)):
        add(trapezoid_pt, rotation=(0, 0, -45))
        add(trapezoid_pt, rotation=(0, 0, 45))

    # Tabs (to prevent wrong insertion).
    with BuildSketch(Plane.XY.offset(TRAPEZ_HEIGHT)):
        cos45 = math.cos(math.radians(45))
        width = (cos45 * TRAPEZ_TIP_WIDTH) + (cos45 * TRAPEZ_WIDTH/2)
        height = TRAPEZ_TIP_WIDTH - TRAPEZ_WIDTH
        Rectangle(width*2, height*2)
    extrude(amount=-TABS_Z_LEN)


if __name__ == '__main__':
    from common.vscode import show_object
    show_object(chex)
    print(f"Volume: {chex.part.volume}")
    # export_stl(chex.part, 'stl/test_hex.stl')
