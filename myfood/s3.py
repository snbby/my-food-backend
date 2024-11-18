import re
from typing import Any, AnyStr
from uuid import uuid4

import boto3
from django.conf import settings


class S3Client:
    AWS_REGION_NAME = 'eu-cental-1'
    AWS_S3_BUCKET_NAME = 'me-proj'
    AWS_S3_HOST = f'https://{AWS_S3_BUCKET_NAME}.s3.eu-central-1.amazonaws.com'
    AWS_S3_DEFAULT_ACL = 'public-read'

    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=settings.MYFOOD_AWS_ACCESS_KEY,
            aws_secret_access_key=settings.MYFOOD_AWS_SECRET_ACCESS_KEY,
        )

    def upload(self, path: str, content: AnyStr) -> str:
        self.client.put_object(
            Body=content, Bucket=self.AWS_S3_BUCKET_NAME, Key=path, ACL=self.AWS_S3_DEFAULT_ACL
        )
        return self.get_link(path)
    
    def upload_fileobj(self, content: Any, bucket: str, path: str) -> str:
        """
        Sample response link: https://me-proj.s3.eu-central-1.amazonaws.com/ava.png
        
        """
        self.client.upload_fileobj(content, bucket, path)
        
        return self.get_link(path=path)

    def delete(self, url: str):
        path = self.extract_path_from_url(url)
        self.client.delete_object(Bucket=self.AWS_S3_BUCKET_NAME, Key=path)

    def is_s3_link(self, url: str) -> bool:
        try:
            self.extract_path_from_url(url)
            return True
        except Exception:
            return False

    def extract_path_from_url(self, url: str) -> str:
        escaped_bucket = self.AWS_S3_BUCKET_NAME.replace('.', r'\.')
        result = re.findall(f'{escaped_bucket}/([0-9a-zA-Z_/.]+)', url)
        if len(result) > 0:
            return result[0]
        else:
            raise Exception(f'This is not an s3 url: {url}. Cannot delete s3 asset')

    def copy(self, url: str) -> str:
        path = self.extract_path_from_url(url)
        new_path = path.rsplit('/', 1)[0] + f'/{uuid4().hex}'
        self.client.copy_object(
            ACL='public-read',
            Bucket=self.AWS_S3_BUCKET_NAME,
            CopySource={'Bucket': self.AWS_S3_BUCKET_NAME, 'Key': path},
            Key=new_path,
        )
        return self.get_link(new_path)

    def get_link(self, path: str) -> str:
        return f'{self.AWS_S3_HOST}/{path}'

    def get_upload_link(self, file_name: str, expiration: int = 300) -> str:
        return self.client.generate_presigned_url(
            'put_object',
            Params={'Bucket': self.AWS_S3_BUCKET_NAME, 'Key': file_name, 'ACL': self.AWS_S3_DEFAULT_ACL},
            ExpiresIn=expiration,
        )

s3_client = S3Client()
