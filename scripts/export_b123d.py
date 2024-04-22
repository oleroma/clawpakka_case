from build123d import Axis, Plane, export_stl, export_step

# Import parts.
import sys
sys.path.insert(1, './build123d')
from wheel import wheel, core, holder

STL_DIR = 'stl/'
STEP_DIR = 'step/'

def export(obj, filename):
    export_stl(obj, STL_DIR + filename + '.stl')
    export_step(obj, STEP_DIR + filename + '.step')

# Scroll wheel.
export(wheel.part, 'secondary_015mm_wheel')
export(core.part.rotate(Axis.X, 90), 'secondary_007mm_wheel_core')
export(holder.part, 'any_015mm_wheel_holder')
