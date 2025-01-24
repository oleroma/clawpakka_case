from build123d import (
    BuildPart, BuildSketch, BuildLine, Box, Plane, Polyline, Rectangle, Location, Locations,
    Axis, Rot, Mode, Align, Until,
    mirror, make_face, extrude, fillet, chamfer, split, faces, add)

COVER_BOTTOM_WIDTH = 62
COVER_BOTTOM_DEPTH = 37
COVER_BOTTOM_HEIGHT = 1.6

TRAPEZ_WIDTH = 25
TRAPEZ_PTS = ((0, 0), (TRAPEZ_WIDTH, 0), (20, 5), (5, 5), (0, 0))

BOX_WIDTH = 6
BOX_DEPTH = 6
BOX_HEIGHT = 8
BOX_INSET = 8  # From outside

USE_TABS = True
TAB_WIDTH = 4
TAB_HEIGHT = 2
TAB_ANGLE = 5  # Degrees.

FILLET_SIZE = 2
CHAMFER_SIZE = 0.5


with BuildPart() as cover:
    # Base.
    with BuildSketch():
        Rectangle(COVER_BOTTOM_WIDTH, COVER_BOTTOM_DEPTH)
    extrude(amount=COVER_BOTTOM_HEIGHT)
    split(bisect_by=Plane.YZ)  # keep only half, since everything will be mirrored in the end

    # Trapezoid.
    plane = Plane.XZ.offset(-COVER_BOTTOM_DEPTH / 2)
    with BuildSketch(plane) as poly_sk:
        with BuildLine(Location((COVER_BOTTOM_WIDTH / 2 - TRAPEZ_WIDTH, COVER_BOTTOM_HEIGHT))):
            Polyline(TRAPEZ_PTS)
        make_face()
    extrude(amount=COVER_BOTTOM_HEIGHT)

    # Trapezoid tabs.
    if USE_TABS:
        trapezoid_face = poly_sk.sketch.face().center()
        # Manually construct a plane with some of the face center coordinates.
        plane = Plane(origin=(
            trapezoid_face.X,
            trapezoid_face.Y,
            COVER_BOTTOM_HEIGHT + 2),
            x_dir=(-1, 0, 0),
            z_dir=(0, 1, 0),
        )
        with BuildSketch(plane.rotated((TAB_ANGLE, 0, 0))): # create sketch on plane rotated about local y-axis
            Rectangle(TAB_WIDTH, TAB_HEIGHT, align=(Align.CENTER, Align.MAX)) # align top edge to y-axis
        extrude(until=Until.PREVIOUS)

    # Box.
    with BuildPart() as box_pt:
        with BuildSketch() as s:
            x = COVER_BOTTOM_WIDTH / 2 - BOX_INSET - BOX_WIDTH / 2
            y = -COVER_BOTTOM_DEPTH / 2 - BOX_WIDTH / 2
            with Locations((x, y)):
                Rectangle(BOX_WIDTH, BOX_DEPTH)
        extrude(amount=BOX_HEIGHT)

    # Box tabs.
    if USE_TABS:
        face_inside = faces().filter_by(Axis.X)[0]
        face_outside = faces().filter_by(Axis.X)[-1]
        plane_inside = Plane(face_inside).rotated((180, -TAB_ANGLE, 0))
        plane_outside = Plane(face_outside).rotated((0, -TAB_ANGLE, 0))
        with BuildSketch(plane_inside):
            Rectangle(TAB_WIDTH, TAB_HEIGHT, align=(Align.CENTER, Align.MAX))
        with BuildSketch(plane_outside):
            Rectangle(TAB_WIDTH, TAB_HEIGHT, align=(Align.CENTER, Align.MAX))
        extrude(until=Until.PREVIOUS)

    # Fillet trapezoid sides.
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[2][0]
    fillet(edges, FILLET_SIZE)

    # Fillet boxes side.
    edges = cover.part.edges().filter_by(Axis.X).group_by(Axis.Y)[1][1]
    fillet(edges, FILLET_SIZE)

    # Chamfer box top.
    edges = cover.part.edges().filter_by(Axis.Z, reverse=True).group_by(Axis.Z)[-1]
    chamfer(edges, CHAMFER_SIZE)

    # Mirror everything.
    mirror(about=Plane.YZ)


if __name__ == '__main__':
    from common.vscode import show_object
    show_object(cover)
    print(f"Volume: {cover.part.volume}")
