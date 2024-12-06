import boto3
import logging, traceback
from botocore.exceptions import NoCredentialsError
from urllib.parse import urljoin

# self.fctaws = fctaws(bucket_name='listreports-ext-listings', access_key='AKAKAKAKAKAKAK', secret_key='8v/+8i8i8i8i8i8i//SN+sN/bNbNbNbNbNbN')
# tab_file = self.fctaws.check_all_file_aws()
# post_image_aws = self.fctaws.upload(local_file=f'images/{local_file}', aws_file=f'social/facebook/images/{username}_{post_id}.jpg')

# __all__ = [
#     name for name, obj in globals().items()
#     if callable(obj) or isinstance(obj, type)  # Include functions and classes
# ]

class fctaws:

    def __init__(self, bucket_name, access_key, secret_key):
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key

    def upload(self, local_file, aws_file):
        file_link = ''
        try:
            if local_file:

                s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

                try:
                    s3.upload_file(local_file, self.bucket_name, aws_file, ExtraArgs={'ACL': 'public-read'})
                    file_link = urljoin(f"https://{self.bucket_name}.s3-us-west-2.amazonaws.com", aws_file)
                    logging.info(f'Upload Successful file_link: {file_link}')
                except FileNotFoundError:
                    logging.warning(f'The file was not found')
                except NoCredentialsError:
                    logging.warning(f'Credentials not available')

        except:
            logging.error(traceback.format_exc())

        return file_link

    def download(self, local_file, aws_file):
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
            s3.download_file(self.bucket_name, aws_file, local_file)
        except:
            logging.error(traceback.format_exc())

    def check_all_file_aws(self, prefix=''):
        tab = []
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
            objects = s3.list_objects(Bucket=self.bucket_name, Prefix=prefix)#prefix='dls/social/agents/'
            for obj in objects.get('Contents'):
                if '.csv' in  obj.get('Key'):
                    tab.append(obj.get('Key'))
        except:
            logging.error(traceback.format_exc())

        return tab

    def check_one_file_aws(self, aws_file):
        file_exist = False
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
            obj_status = s3.list_objects(Bucket=self.bucket_name, Prefix=aws_file)
            if obj_status.get('Contents'):
                file_exist = True
            else:
                file_exist = False
        except:
            logging.error(traceback.format_exc())

        return file_exist

    def delete_bucket_aws(self):
        try:
            s3 = boto3.resource('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
            bucket = s3.Bucket(self.bucket_name)
            counts = sum(1 for _ in bucket.objects.all())
            print(f"files counts: {counts}")
            bucket.objects.all().delete()
            print("bucket emptied.")
        except:
            logging.error(traceback.format_exc())
