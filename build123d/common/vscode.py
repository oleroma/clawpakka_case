try:
    print('OCP_VSCODE: Loading...')
    from ocp_vscode import set_defaults, Camera, show_object
    set_defaults(reset_camera=Camera.KEEP)
    # TODO: Naming sidebar objects.
    print('OCP_VSCODE: Loaded')
except Exception as error:
    print(f'OCP_VSCODE: Error ({error})')
