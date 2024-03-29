## SleepyDrive
An edited version of [AirDrive](https://github.com/jnsougata/AirDrive) made for personal use but anyone can use it! 
Its a simpler version made for easy access. It only supports private drives.

## Installation
### `pip install git+https://github.com/SlumberDemon/SleepyDrive`

## Import
### `from sleepydrive import SleepyDrive`

## Creating New Account
### `drive = SleepyDrive.create(silent = True)`
- Parameters:
  - **private_key**: https://deta.sh project key 
  - **drive_name**: The name your drive will have
  - **silent** (bool): If True, it will not show any prompts (default: False)
  - **raises**: `UnableToCreate` , `DriveNotFound`

## Logging In
### `drive = SleepyDrive.login(username, password, silent = True)`
- Parameters:
  - **private_key**: https://deta.sh project key 
  - **drive_name**: The name of the drive to login
  - **silent** (bool): If True, it will not show any prompts (default: False)
  - **raises**: `UnableToCreate` , `DriveNotFound`

## Methods

### `files`  
- `files()`
  - #### Returns:
    Returns list of file names existing in the drive
### `create_folder`
- `create_folder(folder_name)`
  - Parameters:
  - **folder_name** (str): Name of the folder to be created
  - #### Returns:
    Returns the name of the folder created
### `download`
- `download(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be downloaded
    - #### Returns:
      Returns None & downloads the file to the current directory
    - #### Raises:
      - `FileNotFound`
### `download_all`
- `download_all()`
    - #### Returns:
      - Downloads all files in the drive to the current directory
### `upload`
- `upload(remote_file_name, )`
    - Parameters:
      - **remote_file_name** (str): The name with the file to be uploaded
      - **folder_name** (str): The name of the folder to upload the file to (optional)
      - **local_file_path** (str): Path to the file to be uploaded (optional)
      - **file_content** (Union[bytes | str | io.TextIOBase | io.BufferedIOBase | io.RawIOBase]): Content of the file to be uploaded (optional)
      - Note: If `local_file_path` is not provided, `file_content` must be provided. Do not mix both.
    - #### Returns:
      Returns None & uploads the file to the drive
    - #### Raises:
      - `InvalidFile`
    - ### Note:
      - If the file already exists in the drive, it will be overwritten
### `upolad_from_url`
- `upload_from_url(url, file_name, folder_name)`
    - Parameters:
      - **url** (str): URL of the file to be uploaded
      - **file_name** (str): The name with the file to be uploaded
      - **folder_name** (str): The name of the folder to upload the file to(optional)
    - #### Returns:
      Returns the file content (bytes)
    - ### Raises:
      - `InvalidURL`
    - ### Note:
      - If the file already exists in the drive, it will be overwritten
### `rename`
- `rename(old_file_name, new_file_name)`
    - Parameters:
      - **old_file_name** (str): The old name of file to be renamed
      - **new_file_name** (str): New name of the file
    - #### Returns:
      Returns None & re-uploads the file in the drive with new name
    - #### Raises:
      - `FileNotFound`
    - ### Note:
      - Might take a while for large files
### `cache`
- `cache(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be cached
    - #### Returns:
      Returns the file content as bytes
    - ### Raises:
      - `FileNotFound`
### `file_stream`
- `file_stream(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be streamed
    - #### Returns:
      Returns the file content as streaming body
    - ### Raises:
      - `FileNotFound`
### `delete`
- `delete(file_name)`
    - Parameters:
      - **file_name** (str): Name of the file to be deleted
    - #### Returns:
      Returns None & deletes the file from the drive permanently
### `delete_all`
- `delete_all()`
    - #### Returns:
      Returns None & deletes all files from the drive permanently
### `delete_account`
- `delete_account()`
    - #### Returns:
      Returns None & deletes the account from the drive permanently
    - ### Raises:
      - `AccountNotFound`