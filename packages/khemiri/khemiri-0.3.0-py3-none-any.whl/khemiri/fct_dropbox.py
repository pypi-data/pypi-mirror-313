import dropbox
import logging
import os
import traceback

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class DropboxSender:
    def __init__(self, local_file_path, dropbox_file_path, dropbox_token):
        self.local_file_path = local_file_path
        self.dropbox_file_path = dropbox_file_path
        self.dropbox_token = dropbox_token
        self.dbx = dropbox.Dropbox(self.dropbox_token)

        logging.info(f'local_file_path: {self.local_file_path}')
        logging.info(f'dropbox_file_path: {self.dropbox_file_path}')


    # def create_folder(self, folder_path):
    #     """Creates a folder in Dropbox at the specified path if it doesn't already exist."""
    #     try:
    #         folder_name = os.path.basename(folder_path)
    #         parent_path = os.path.dirname(folder_path)
    #         result = self.dbx.files_list_folder(parent_path)
    #
    #         for entry in result.entries:
    #             if isinstance(entry, dropbox.files.FolderMetadata) and entry.name == folder_name:
    #                 logging.warning(f'Folder already exists: {folder_path}')
    #                 return
    #
    #         self.dbx.files_create_folder_v2(folder_path)
    #         logging.info(f'Folder created at: {folder_path}')
    #
    #     except:
    #         logging.error(traceback.format_exc())

    def send_file(self):
        CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB

        if os.path.exists(self.local_file_path):
            try:
                logging.info(f'Attempting to upload file to Dropbox at path: {self.dropbox_file_path}')

                if not self.dropbox_file_path.startswith('/'):
                    raise ValueError('Dropbox file path must start with a "/"')

                file_size = os.path.getsize(self.local_file_path)
                uploaded_size = 0

                with open(self.local_file_path, 'rb') as f:
                    if file_size <= CHUNK_SIZE:
                        # File is small enough to upload in one go
                        self.dbx.files_upload(f.read(), self.dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)
                        uploaded_size = file_size
                        logging.info(f'Uploaded {uploaded_size}/{file_size} bytes (100%)')
                    else:
                        # Start a session for chunked upload
                        upload_session_start_result = self.dbx.files_upload_session_start(f.read(CHUNK_SIZE))
                        uploaded_size += CHUNK_SIZE
                        logging.info(f'Uploaded {uploaded_size}/{file_size} bytes ({(uploaded_size / file_size) * 100:.2f}%)')

                        cursor = dropbox.files.UploadSessionCursor(
                            session_id=upload_session_start_result.session_id,
                            offset=f.tell()
                        )
                        commit = dropbox.files.CommitInfo(path=self.dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)

                        while f.tell() < file_size:
                            remaining_size = file_size - f.tell()
                            if remaining_size <= CHUNK_SIZE:
                                # Final chunk
                                self.dbx.files_upload_session_finish(f.read(remaining_size), cursor, commit)
                                uploaded_size += remaining_size
                            else:
                                # Append chunk
                                self.dbx.files_upload_session_append_v2(f.read(CHUNK_SIZE), cursor)
                                cursor.offset = f.tell()
                                uploaded_size += CHUNK_SIZE

                            # Log progress
                            logging.info(f'Uploaded {uploaded_size}/{file_size} bytes ({(uploaded_size / file_size) * 100:.2f}%)')

                logging.info(f'File "{self.local_file_path}" successfully uploaded to Dropbox as "{self.dropbox_file_path}"')

            except:
                logging.error(traceback.format_exc())

        else:
            logging.warning(f'File "{self.local_file_path}" not found')


    def send_file_old(self):
        shared_link = None
        if os.path.exists(self.local_file_path):
            try:
                # dropbox_folder_path = os.path.dirname(self.dropbox_file_path)
                # self.create_folder(dropbox_folder_path)
                logging.info(f'Attempting to upload file to Dropbox at path: {self.dropbox_file_path}')

                if not self.dropbox_file_path.startswith('/'):
                    raise ValueError('Dropbox file path must start with a "/"')

                with open(self.local_file_path, 'rb') as f:
                    self.dbx.files_upload(f.read(), self.dropbox_file_path, mode=dropbox.files.WriteMode.overwrite)

                logging.info(f'File "{self.local_file_path}" uploaded to Dropbox as "{self.dropbox_file_path}"')

                # # Try to create a shared link or retrieve an existing one
                # try:
                #     shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(self.dropbox_file_path)
                #     shared_link = shared_link_metadata.url
                # except dropbox.exceptions.ApiError as e:
                #     if e.error.is_shared_link_already_exists():
                #         shared_link_metadata = self.dbx.sharing_list_shared_links(self.dropbox_file_path).links[0]
                #         shared_link = shared_link_metadata.url
                #         logging.info(f'Shared link already exists. Retrieved existing link: {shared_link}')
                #     else:
                #         raise

            except:
                logging.error(traceback.format_exc())

        return shared_link  # Return the shared link


# Example usage:
# https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps
# application: uploader_khemiri

# from assets.fct.fctdropbox import DropboxSender
# local_file_path = os.path.join(base_dir, file_name)
# dropbox_file_path = f'/folder/{file_name}'
# dropbox_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# DropboxSender(local_file_path, dropbox_file_path, dropbox_token).send_file()
