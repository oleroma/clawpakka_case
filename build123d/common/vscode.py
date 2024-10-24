try:
    print(f'Loading ocp_vscode...')
    from ocp_vscode import set_defaults, Camera, show_object
    set_defaults(reset_camera=Camera.KEEP)
    # TODO: Naming sidebar objects.
    print(f'Loading ocp_vscode complete')
except Exception as error:
    print(f'ocp_vscode error ({error})')
