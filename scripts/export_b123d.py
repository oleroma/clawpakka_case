from build123d import Axis, Plane, Compound, Location, export_stl, export_step

# Import parts.
import sys
sys.path.insert(1, './build123d')
from button_dpad import button_dpad
from button_abxy import button_abxy
from button_select import button_select
from thumbstick_right import thumbstick_right
from wheel import wheel_default, wheel_loose, wheel_tight
from wheel_core import core
from wheel_holder import holder
from trigger_r1 import trigger_r1
from cover import cover
from hexagon import chex
from dongle_case import dongle_case

STL_DIR = 'stl/'
STEP_DIR = 'step/'

def export(obj, filename, subdir=''):
    print(f'Exporting {filename}')
    export_stl(obj, STL_DIR + subdir + filename + '.stl')
    export_step(obj, STEP_DIR + subdir + filename + '.step')

# Buttons.
export(button_abxy.part, '007mm_abxy_4x')
export(button_dpad.part, '007mm_dpad_4x')
export(button_select.part, '007mm_select_4x')

# Trigger L1/R1.
export(trigger_r1.part, '015mm_trigger_R1')
export(trigger_r1.part.mirror(Plane.YZ), '015mm_trigger_L1')

# Scroll wheel.
export(wheel_default.part, '015mm_wheel')
export(wheel_loose.part, '015mm_wheel_loose', 'variants/')
export(wheel_tight.part, '015mm_wheel_tight', 'variants/')
export(core.part.rotate(Axis.X, 90), '007mm_wheel_core')
export(holder.part, '015mm_wheel_holder')

# Battery Cover.
export(cover.part, '015mm_cover')

# Conductive Hex.
export(chex.part, '015mm_hexagon_CONDUCTIVE')

# Thumbstick right.
export(thumbstick_right.part, '007mm_thumbstick_R')

# Dongle case.
export(dongle_case.part, '015mm_dongle_case')
