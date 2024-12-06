import logging, traceback
from google.oauth2 import service_account
from google.cloud import storage

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class fctGCP:

    def __init__(self, file_path, bucket_name, service_account_file):
        self.file_path = file_path
        self.bucket_name = bucket_name
        self.service_account_file = service_account_file

    def upload_to_gcp(self, remote_name=None):
        link_gcp = ''
        try:
            credentials = service_account.Credentials.from_service_account_file(self.service_account_file)
            client = storage.Client(credentials=credentials)
            bucket = client.get_bucket(self.bucket_name)
            remote_name = remote_name if remote_name else self.file_path.split("/")[-1]
            blob = bucket.blob(remote_name)
            blob.upload_from_filename(self.file_path)
            link_gcp = blob.public_url
        except:
            logging.warning(f"Failed to upload file {self.file_path} to {remote_name}")
            logging.error(traceback.format_exc())

        return link_gcp


# if __name__ == '__main__':
#     file_path = 'results.csv'
#     link_gcp = UploadGCP(file_path=file_path, bucket_name='automatiq-scrapes', service_account_file='private_key.json').upload_to_gcp()
#     logging.info(f'link_gcp: {link_gcp}')


