print('OCP_VSCODE: Loading...')
from ocp_vscode import set_defaults, Camera, show_object

# Do not reset camera.
set_defaults(reset_camera=Camera.KEEP)
