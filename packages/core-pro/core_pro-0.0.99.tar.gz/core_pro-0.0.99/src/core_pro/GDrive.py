import io
import polars as pl
import mimetypes
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path
from time import perf_counter
from .config import GoogleAuthentication
from rich import print


class Drive(GoogleAuthentication):
    def __init__(self, debug: bool = True):
        super().__init__('drive')
        self.debug = debug
        self.status = '[orange]🦑 Drive[/orange]'

    def upload(
            self,
            file_dir: Path,
            folder_id: str,
            name_on_drive: str = None,
    ) -> dict:
        """Upload to drive"""
        # count time
        start = perf_counter()
        # init
        if not name_on_drive:
            name_on_drive = file_dir.name
        file_dir = file_dir.resolve()
        file_size = float(file_dir.stat().st_size) / 1024**2  # MB
        # get info
        body = {'name': name_on_drive, 'parents': [folder_id]}
        content_type, _ = mimetypes.guess_type(file_dir)
        media = MediaFileUpload(file_dir, mimetype=content_type, resumable=True)
        fields = 'webContentLink, id, webViewLink'
        # upload
        file = self.service.files().create(body=body, media_body=media, fields=fields, supportsAllDrives=True).execute()
        if self.debug:
            print(f"{self.status} Upload to f_id: {folder_id} - Size: {file_size:,.0f}MB")
        # log
        dict_log = {
            'f_id': file,
            'size': file_size,
            'path': file_dir,
            'upload_time': perf_counter() - start,
        }
        return dict_log

    def get_file_info(self, file_id: str):
        fields = 'id,name,mimeType,kind,size,fileExtension'
        return self.service.files().get(fileId=file_id, fields=fields, supportsAllDrives=True).execute()

    def drive_download(
            self,
            file_id: str,
            download_dir: str
    ) -> dict:
        """Download from drive"""
        # count time
        start = perf_counter()
        # get info
        file_info = self.get_file_info(file_id)
        file_size = float(file_info['size']) / 1024 ** 2  # MB
        save_path = f"{download_dir}/{file_info['name']}"
        # check exist
        if Path(save_path).exists():
            print(f"{self.status} File is already exist: {save_path}")
        else:
            # download
            request = self.service.files().get_media(fileId=file_id)
            fh = io.FileIO(save_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            if self.debug:
                print(f"{self.status} Download {file_id} path: {save_path} - Size: {file_size:,.0f}MB")
            # progress
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Progress - {int(status.progress() * 100)}%")
        # log
        dict_log = {
            'path': save_path,
            'download_time': perf_counter() - start,
            'size': file_size,
        }
        return dict_log

    def create_new_folder(
            self,
            name: str,
            parent_id=None
    ):
        """
        create new folder on Google Drive
        :param name: Name of folder
        :param parent_id: id of parent folder , default None
        :return: return folder id if True
        """

        body = {
            'name': name,
            'parents': [parent_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if not parent_id:
            body.pop('parents')
        file = self.service.files().create(body=body, fields='id', supportsAllDrives=True).execute()
        print(f"{self.status} Successfully created folder: {name} - Folder ID: {file.get('id')}")
        return file.get('id')

    def rename_file(self, file_id: str, new_name: str):
        file = {'name': new_name}
        self.service.files().update(fileId=file_id, body=file).execute()

    def remove_file(self, file_id: str, move_to_trash: bool = True):
        if move_to_trash:
            body_value = {'trashed': True}
            resp = self.service.files().update(fileId=file_id, body=body_value, supportsAllDrives=True).execute()
        else:
            resp = self.service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        print(f"{self.status} Remove: {file_id} Trash: {move_to_trash}")
        return resp

    def empty_trash(self):
        resp = self.service.files().emptyTrash().execute()
        print(f"{self.status} Empty trash")
        return resp

    def download_gsheet(self, file_id, file_location, file_name, file_type):
        request = self.service.files().export_media(fileId=file_id, mimeType=file_type)
        fh = io.FileIO(file_location + file_name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

    def search_files(self, folder_id: str):
        fields = 'nextPageToken, files(id, name, createdTime, modifiedTime)'
        query = f"'{folder_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query, fields=fields, includeItemsFromAllDrives=True, supportsAllDrives=True
        ).execute()
        return results.get('files', [])

    def share_file(
            self,
            file_id,
            email: str = None,
            role: str = 'reader',
            domain: str = '@shopee.com'
    ):
        """
        :param file_id: abc
        :param email: abc@example.com
        :param role: reader/writer
        :param domain: @example.com
        :return: text
        """
        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f"Request_Id: {request_id}")
                print(f'Permission Id: {response.get("id")}')
                ids.append(response.get("id"))

        ids = []
        batch = self.service.new_batch_http_request(callback=callback)
        if email:
            body = {
                "type": "user",
                "role": role,
                "emailAddress": email,
            }
            batch.add(self.service.permissions().create(fileId=file_id, body=body, fields="id", supportsAllDrives=True))
        else:
            body = {
                "type": "domain",
                "role": role,
                "domain": domain,
            }
            batch.add(self.service.permissions().create(fileId=file_id, body=body, fields="id"))
        batch.execute()
        print(f"{self.status} Shared {body['type']} {body.get('emailAddress', 'domain')}: {file_id}")

    def remove_share_publicly(self, file_id: str):
        body = 'anyoneWithLink'
        self.service.permissions().delete(fileId=file_id, permissionId=body, fields='id', supportsAllDrives=True).execute()
        print(f"{self.status} Removed sharing: {file_id}")

    def remove_duplicates(self, file_id: str):
        lst = self.search_files(file_id)
        all_files = (
            pl.DataFrame(lst)
            .with_columns(
                pl.col(i).str.strptime(pl.Datetime, strict=False)
                for i in ['createdTime', 'modifiedTime']
            )
            .sort(['name', 'createdTime'], descending=True)
            .with_columns(
                pl.col('createdTime').rank(method='max', descending=True).over('name').alias('rank')
            )
            .to_dicts()
        )
        for f in all_files:
            if f['rank'] != 1:
                Drive().remove_file(f['id'])
