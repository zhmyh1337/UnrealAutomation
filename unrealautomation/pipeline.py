import unrealautomation.uat_package as uat_package
import unrealautomation.git_switch_and_pull as git_switch_and_pull
import unrealautomation.archive as archive
import unrealautomation.generate_output_paths as generate_output_paths
import unrealautomation.clean_output_dir as clean_output_dir
import unrealautomation.ydisk_upload as ydisk_upload
import unrealautomation.discord_message as discord_message
import unrealautomation.wait_for_user_input as wait_for_user_input


ACTIONS = [
    git_switch_and_pull,
    generate_output_paths,
    clean_output_dir,
    uat_package,
    archive,
    wait_for_user_input,
    ydisk_upload,
    discord_message
]

def execute_pipeline():
    for action in ACTIONS:
        print(f'EXECUTING {action.__name__}:')
        action_result = action.execute()
        print()
        if not action_result:
            print(f'\aFAILED TO EXECUTE {action.__name__}')
            return False

    print('\aPIPELINE COMPLETED')
    return True
