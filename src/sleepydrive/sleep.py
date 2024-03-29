import io
from .dcd import *
from .errors import *
from deta import Deta
from typing import Union
from binascii import unhexlify
from time import perf_counter
from urllib3 import PoolManager


class SleepyDrive:
    def __init__(self, drive: Deta.Drive, silent: bool = False):
        self.__drive = drive
        self.__silent = silent
        self.__http = PoolManager()

    def __repr__(self):
        return f"<SleepyDrive>"

    def __log(self, prompt: str) -> None:
        if not self.__silent:
            print(prompt)

    @classmethod
    def create(cls, private_key: str, drive_name: str, silent: bool = False):
        """
        Create a new drive
        :param private_key: https://deta.sh project key
        :param drive_name: The name your drive will have
        :param silent: if True, prompt will be shown
        :return: SleepyDrive object
        """
        key = private_key if private_key else PK
        try:
            drive = Deta(key).Drive(drive_name)
            files = drive.list().get('names')
            if files:
                return cls.login(private_key)
            if not silent:
                print(f"Drive created")
            drive.put(name='.air', data=b' ')
            return cls(drive=drive, silent=silent)
        except:
            raise UnableToCreate("Unable to create drive")

    @classmethod
    def login(cls, private_key: str, drive_name: str, silent: bool = False):
        """
        Login to an existing drive
        :param private_key: https://deta.sh project key
        :param drive_name: The name of the drive to login
        :param silent: if True, prompt will be shown
        :return: SleepyDrive object
        """
        key = private_key if private_key else PK
        try:
            drive = Deta(key).Drive(drive_name)
            files = drive.list().get('names')
            if files:
                if not silent:
                    print(f"Logged in")
                    print('-------')
                return cls(drive=drive, silent=silent)
            else:
                raise DriveNotFound(f"Drive doesn't exist")
        except:
            raise UnableToCreate("Unable to create drive")

    def files(self) -> list:
        """
        :return: list of files in the account
        """
        files = self.__drive.list().get('names')
        try:
            files.remove('.air')
            return files
        except ValueError:
            return files

    def create_folder(self, folder_name: str) -> None:
        """
        Create a new folder in the drive
        :param folder_name: the name of the folder to create
        :return: None
        """
        path = f'{folder_name}/.air'
        self.__drive.put(name=path, data=b' ')
        self.__log(f"[+] Created folder ({folder_name})")

    def upload(
            self,
            remote_file_name: str,
            folder_name: str = None,
            local_file_path: str = None,
            file_content: Union[bytes, str, io.TextIOBase, io.BufferedIOBase, io.RawIOBase] = None
    ) -> None:
        """
        Upload a file to the drive
        :param local_file_path: path to the local file
        :param remote_file_name: name with which the file will be saved on the drive
        :param folder_name: folder in which the file will be saved on the drive (optional)
        :param file_content: content of the file to be sent (optional)
        :return: None
        """
        if local_file_path:
            with open(local_file_path, "rb") as f:
                content = f.read()
        elif file_content:
            content = file_content
        else:
            raise InvalidFile("You must specify a (local_file_path) or (file_content). Do not mix both.")
        if folder_name:
            path = f'{folder_name}/{remote_file_name}'.replace('//', '/')
        else:
            path = remote_file_name
        self.__log(f'[↑] Uploading | {path} | ...')
        timer_start = perf_counter()
        self.__drive.put(name=path, data=content)
        timer_end = perf_counter()
        elapsed = round(timer_end - timer_start)
        self.__log(f"[•] Completed | {path} | {round(len(content) * 10 ** (-6), 3)} MB | {elapsed}s")

    def upload_from_url(
            self,
            url: str,
            file_name: str,
            folder_name: str = None
    ) -> bytes:
        """
        Upload a file from a URL to the drive
        :param url: URL from which the file content will be downloaded
        :param file_name: name with which the file will be saved on the drive
        :param folder_name: folder in which the file will be saved on the drive (optional)
        :return: None
        """
        if folder_name:
            path = f'{folder_name}/{file_name}'.replace('//', '/')
        else:
            path = file_name
        timer_start = perf_counter()
        try:
            r = self.__http.request('GET', url)
        except Exception:
            raise InvalidURL("Either given URL is not valid or the file is not accessible")
        self.__log(f'[↑] Uploading | {path} | ...')
        content = r.data
        self.__drive.put(name=path, data=content)
        timer_end = perf_counter()
        elapsed = round(timer_end - timer_start)
        self.__log(f"[•] Completed | {path} | {round(len(content) * 10 ** (-6), 3)} MB | {elapsed}s")
        return content

    def rename(self, old_name: str, new_name: str) -> None:
        """
        Rename a file on the drive
        :param old_name: old name of the file
        :param new_name: new name of the file to be saved
        :return: None
        """
        content = self.__drive.get(old_name)
        if content:
            self.__drive.put(name=new_name, data=content)
            self.__log(f"[!] Renamed | ({old_name}) -> ({new_name})")
            self.__drive.delete(old_name)
        else:
            raise FileNotFound(f'file ({old_name}) does not exist')

    def download(self, file_name: str) -> None:
        """
        Download a file from the drive
        :param file_name: name/path of the file to download
        :return: None
        """
        resp = self.__drive.get(file_name)
        if resp:
            self.__log(f'[↓] Downloading | {file_name} | ...')
            timer_start = perf_counter()
            with open(file_name, "wb") as f:
                size = 0
                for chunk in resp.iter_chunks(1024):
                    if chunk:
                        size += len(chunk)
                        f.write(chunk)
            timer_end = perf_counter()
            elapsed = round(timer_end - timer_start)
            self.__log(f"[•] Completed | {file_name} | {round(size * 10 ** (-6), 3)} MB | {elapsed}s")
        else:
            raise FileNotFound(f"file ({file_name}) does not exist")

    def file_stream(self, file_name: str) -> bytes:
        """
        Download a file from the drive and return its content (streamable)
        :param file_name: name/path of the file to stream
        :return: bytes
        """
        stream = self.__drive.get(file_name)
        if stream:
            return stream
        raise FileNotFound(f"file ({file_name}) does not exist")

    def cache(self, file_name: str) -> bytes:
        """
        Download a file from the drive and return its content (bytes)
        :param file_name: name/path of the file to cache
        :return: bytes
        """
        resp = self.__drive.get(file_name)
        if resp:
            self.__log(f'[🗎] Caching | {file_name} | ...')
            timer_start = perf_counter()
            byte_list = [chunk for chunk in resp.iter_chunks(1024)]
            content = b''.join(byte_list)
            timer_end = perf_counter()
            elapsed = round(timer_end - timer_start)
            self.__log(f'[🗎] Completed | {file_name} | {round(len(content) * 10 ** (-6), 3)} MB | {elapsed}s')
            return content
        raise FileNotFound(f"file ({file_name}) does not exist")

    def download_all(self) -> None:
        """
        Download all files in the account to the current directory
        :return: None
        """
        for file_name in self.files():
            self.download(file_name)

    def delete(self, file_name: str = None) -> None:
        """
        Delete a file from the drive
        :param file_name: file name/path to delete
        :return: None
        """
        if file_name and file_name != '.air':
            self.__drive.delete(file_name)
            self.__log(f"[!] Deleted | ({file_name})")

    def delete_all(self) -> None:
        """
        Delete all files in the drive
        :return: None
        """
        files = self.files()
        try:
            files.remove('.air')
        except ValueError:
            self.__drive.put(name='.air', data=b' ')
        self.__drive.delete_many(files)
        self.__log("[!] Deleted all files")
