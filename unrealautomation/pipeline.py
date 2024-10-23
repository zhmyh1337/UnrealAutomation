import unrealautomation.uat_package as uat_package
import unrealautomation.git_switch_and_pull as git_switch_and_pull
import unrealautomation.archive as archive
import unrealautomation.generate_output_paths as generate_output_paths
import unrealautomation.clean_output_dir as clean_output_dir
import unrealautomation.ydisk_upload as ydisk_upload


ACTIONS = [
    git_switch_and_pull,
    clean_output_dir,
    generate_output_paths,
    uat_package,
    archive,
    ydisk_upload
]

def execute_pipeline():
    for action in ACTIONS:
        print(f'EXECUTING {action.__name__}:')
        action_result = action.execute()
        print()
        if not action_result:
            print(f'FAILED TO EXECUTE {action.__name__}')
            return False

    print('\nPIPELINE COMPLETED')
    return True
