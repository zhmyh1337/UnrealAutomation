# uploading archive to Yandex Disk (requires cloud_api:disk.write and cloud_api:disk.read (for publishing) permissions)

import requests
import os
from . import secrets, config, ctx


def create_directories(path, headers):
    parts = path.strip('/').split('/')
    current_path = ''

    for part in parts:
        current_path += '/' + part
        
        params = {"path": current_path}
        create_folder_response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)

        if not create_folder_response.ok and create_folder_response.json().get('error') != 'DiskPathPointsToExistentDirectoryError':
            print(f'Failed to create folder {current_path} ({create_folder_response.status_code}) ({create_folder_response.text})')
            return False

        if create_folder_response.ok:
            print('Created folder', current_path)
            
    return True

def execute():
    headers = {
        'Authorization': 'OAuth ' + secrets['YdiskToken']
    }

    dir_path = config['YdiskOutputPath'] + '/' + config['TargetName'] + '/'

    if not create_directories(dir_path, headers):
        return False

    path = dir_path + os.path.basename(ctx.archive_path)
    path_with_messed_extension = path + '000' # to avoid throttling when uploading some type of files including .zip

    if not config['YdiskShouldOverwriteExistingFile']: # making sure the file with original extension does not exist to avoid unnecessary uploading
        params = {
            "path": path
        }
        check_file_response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=headers)
        if check_file_response.ok:
            print('The file on Ydisk already exist (you can enable overwriting with YdiskShouldOverwriteExistingFile)')
            return False

    params = {
        "path": path_with_messed_extension,
        "overwrite": config['YdiskShouldOverwriteExistingFile']
    }
    get_upload_url_response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)
    if not get_upload_url_response.ok:
        if get_upload_url_response.json()['error'] == 'DiskResourceAlreadyExistsError':
            print('The file on Ydisk already exist (you can enable overwriting with YdiskShouldOverwriteExistingFile)')
        else:
            print(f'Failed to get upload url ({get_upload_url_response.status_code}) ({get_upload_url_response.text})')
        return False

    print('Got Ydisk upload link')

    with open(ctx.archive_path, 'rb') as f:
        print('Uploading file to Ydisk...')
        upload_response = requests.request(get_upload_url_response.json()['method'], get_upload_url_response.json()['href'], data=f)
    
    if not upload_response.ok:
        print(f'Failed to upload file ({upload_response.status_code}) ({upload_response.text})')
        return False

    print('File uploaded to Ydisk')

    params = {
        "from": path_with_messed_extension,
        "path": path,
        "overwrite": config['YdiskShouldOverwriteExistingFile']
    }
    rename_response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/move', params=params, headers=headers)
    if not rename_response.ok:
        if rename_response.json()['error'] == 'DiskResourceAlreadyExistsError':
            print('The file on Ydisk already exist (you can enable overwriting with YdiskShouldOverwriteExistingFile)')
        else:
            print(f'Failed to rename file ({rename_response.status_code}) ({rename_response.text})')
        return False

    print('Renamed file to have original extension')

    if config['YdiskShouldPublish']:
        params = {
            "path": path
        }
        publish_response = requests.put('https://cloud-api.yandex.net/v1/disk/resources/publish', params=params, headers=headers)

        if not publish_response.ok:
            print(f'Failed to publish file ({publish_response.status_code}) ({publish_response.text})')
            return False

        publish_view_response = requests.request(publish_response.json()['method'], publish_response.json()['href'], headers=headers)
        
        if not publish_view_response.ok:
            print(f'Failed to view published file ({publish_view_response.status_code}) ({publish_view_response.text})')
            return False

        ctx.public_url = publish_view_response.json()['public_url']

        print('Ydisk public url:', ctx.public_url)

    return True
