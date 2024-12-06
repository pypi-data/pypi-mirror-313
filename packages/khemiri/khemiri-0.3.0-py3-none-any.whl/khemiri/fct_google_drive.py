from os.path import dirname, abspath, join
import os, logging, traceback
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from khemiri import fct_core

# from assets.utility.google_drive import GoogleDrive
# google_drive = GoogleDrive()
# google_drive.is_found_folder(folder_name)
# folder_id = google_drive.create_folder(folder_name)
# sub_folder_id = google_drive.create_sub_folder(folder_id, sub_folder_name)
# google_drive.upload_image_to_folder(folder_id=product_name_folder_id, image_path=image_path, image_name=image_name)

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class GoogleDrive:
    def __init__(self):
        path_authentification = join(dirname(abspath(__file__)), "authentification.json")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_authentification
        self.creds, _ = google.auth.default()
        self.service = build('drive', 'v3', credentials=self.creds, cache_discovery=False)

    def format_name(self, folder_name):
        return fct_core.preg_repace(patt=' +', repl='_', subj=fct_core.preg_repace(patt='[^\w\d ]+', repl=' ', subj=folder_name.lower()))


    def delete_folder(self, folder_id):
        try:
            service = self.service.files()
            service.delete(fileId=folder_id).execute()
            logging.info(f'delete_folder: folder_id: {folder_id}')
        except:
            ''

    def is_found_folder(self, folder_name):
        folder_id = ''
        folder_found = False
        folder_name = self.format_name(folder_name)
        try:
            service = self.service.files()
            response = service.list(q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'", spaces='drive').execute()
            items = response.get('files', [])
            if items:
                folder_id = next(iter([item['id'] for item in items if folder_name == item['name']]))
                count = len(items)
                if count > 0:
                    folder_found = True
        except:
            logging.error(traceback.format_exc())

        # logging.info(f'is_found_folder: folder_name: {folder_name} | folder_id: {folder_id} | folder_found: {folder_found}')
        return folder_found, folder_id


    def is_found_file(self, file_name):
        file_id = ''
        file_found = False
        file_name = self.format_name(file_name)
        try:
            service = self.service.files()
            response = service.list(q=f"name='{file_name}'", spaces='drive').execute()
            items = response.get('files', [])
            if items:
                file_id = next(iter([item['id'] for item in items if file_name == item['name']]))
                count = len(items)
                if count > 0:
                    file_found = True
        except:
            logging.error(traceback.format_exc())

        # logging.info(f'is_found_file: file_name: {file_name} | file_id: {file_id} | file_found: {file_found}')
        return file_found, file_id

    def create_folder(self, folder_name):
        folder_found, folder_id = self.is_found_folder(folder_name)
        folder_name = self.format_name(folder_name)
        if not folder_found:
            try:
                service = self.service
                file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder", 'role': 'reader', 'type': 'anyone', "allowFileDiscovery": True}
                folder = service.files().create(body=file_metadata, fields='id').execute()
                folder_id = folder.get('id')
                permission = {
                    'type': 'anyone',
                    'role': 'writer',
                }
                service.permissions().create(fileId=folder_id, body=permission).execute()
            except:
                logging.error(traceback.format_exc())

            logging.info(f'new create_folder: folder_name: {folder_name} | folder_id: {folder_id}')

        else:
            logging.warning(f'exist create_folder: folder_name: {folder_name} | folder_id: {folder_id}')

        return folder_id


    def create_sub_folder(self, folder_id, folder_name):
        sub_folder_found, sub_folder_id = self.is_found_folder(folder_name)
        folder_name = self.format_name(folder_name)
        if not sub_folder_found:
            try:
                service = self.service
                file_metadata = {
                    'name': folder_name,
                    "parents": [folder_id],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = service.files().create(body=file_metadata, fields='id').execute()
                sub_folder_id = folder.get('id')
                permission = {
                    'type': 'anyone',
                    'role': 'writer',
                }
                service.permissions().create(fileId=sub_folder_id, body=permission).execute()
            except:
                logging.error(traceback.format_exc())

            logging.info(f'new create_sub_folder: folder_id: {folder_id} >> folder_name: {folder_name} | sub_folder_id: {sub_folder_id}')

        else:
            logging.warning(f'exist create_sub_folder: folder_id: {folder_id} >> folder_name: {folder_name} | sub_folder_id: {sub_folder_id}')

        return sub_folder_id


    def upload_image_to_folder(self, folder_id, image_path, image_name):
        file_found, file_id = self.is_found_file(image_name)
        if not file_found:
            try:
                service = self.service
                file_metadata = {
                    'name': image_name,
                    'parents': [folder_id]
                }
                media = MediaFileUpload(image_path, mimetype='image/jpeg', resumable=True)
                file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
                file_id = file.get('id')  # Added
                permission = {
                    'type': 'anyone',
                    'role': 'writer',

                }
                service.permissions().create(fileId=file_id, body=permission).execute()
            except:
                logging.error(traceback.format_exc())

            logging.info(f'new upload_to_folder: file_id: {file_id} >> image_name: {image_name}')

        else:
            logging.warning(f'exist upload_to_folder: file_id: {file_id} >> image_name: {image_name}')

        return file_id