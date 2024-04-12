import sys
sys.path.insert(1, './build123d')
from wheel import wheel, core, holder
from build123d import Rotation

STLDIR = 'stl/'
STEPDIR = 'step/'

def export(obj, filename):
    obj.export_stl(STLDIR + filename + '.stl')
    obj.export_step(STEPDIR + filename + '.step')

export(wheel.part, 'secondary_015mm_wheel')
export(Rotation(90, 0, 0) * core.part, 'secondary_007mm_wheel_core')
export(holder.part, 'any_015mm_wheel_holder')
