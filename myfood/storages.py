from django.core.files.storage import Storage
import requests

from myfood.s3 import s3_client


class S3Storage(Storage):
    def save(self, name, content, max_length=None):
        """
        Save new content to the file specified by name. The content should be
        a proper File object or any Python file-like object, ready to be read
        from the beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name
        s3_client.upload_fileobj(content=content, bucket=s3_client.AWS_S3_BUCKET_NAME, path=name)

        return name

    def _open(self, name, mode):
        return requests.get(url=self.url(name)).content
    
    def size(self):
        pass

    def path(self, name: str):
        return 
    
    def delete(self, name: str):
        pass
    
    def exists(self, name: str):
        pass
    
    def listdir(self, path: str):
        pass
    
    def url(self, name):
        """
        Return an absolute URL where the file's contents can be accessed
        directly by a web browser.
        """
        return s3_client.get_link(path=name)
