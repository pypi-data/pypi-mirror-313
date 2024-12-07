import os
from urllib.parse import parse_qs, urlparse

import boto3
from botocore.exceptions import ClientError


class BaseStorage:
    url = None
    options = None
    OPTION_CASTS = {}

    def __init__(self, url):
        self.url = urlparse(url)
        self.query_params = self.url_querystring_to_dict()
        self.options = self.get_options()

    def url_querystring_to_dict(self):
        query_string = self.url.query

        query_dict = parse_qs(query_string)

        for key, value in query_dict.items():
            if len(value) == 1:
                query_dict[key] = value[0]

        return {
            key: self.OPTION_CASTS[key](value) if key in self.OPTION_CASTS else value
            for key, value in query_dict.items()
        }

    def get_options(self):
        return None

    def upload(self, source, target):
        raise NotImplementedError

    def exists(self, target):
        raise NotImplementedError

    def get_url(self, target):
        raise NotImplementedError


class S3Storage(BaseStorage):
    def __init__(self, url):
        super().__init__(url)
        self.client = boto3.client(
            's3',
            endpoint_url=self.options['endpoint_url'],
            aws_access_key_id=self.options['access_key'],
            aws_secret_access_key=self.options['secret_key'],
        )

    def get_options(self):
        base_url = f'https://{self.url.hostname}'
        local_endpoint = self.query_params.get('local_endpoint')
        endpoint_url = f'http://{local_endpoint}' if local_endpoint else base_url
        return {
            'base_url': base_url,
            'endpoint_url': endpoint_url,
            'bucket_name': self.url.path[1:],
            'access_key': self.url.username,
            'secret_key': self.url.password,
            **self.query_params,
        }

    def upload(self, source, target):
        object_name = os.path.join(self.options['location'], target)
        self.client.upload_file(source, self.options['bucket_name'], object_name)
        return self.get_url(target)

    def exists(self, target):
        try:
            self.client.head_object(Bucket=self.options['bucket_name'], Key=target)
            return True
        except ClientError:
            return False

    def get_url(self, target):
        return os.path.join(self.options['base_url'], self.options['bucket_name'], self.options['location'], target)


STORAGE_STORAGES = {
    's3': S3Storage,
}


def get_storage(url):
    storage_scheme = urlparse(url).scheme
    return STORAGE_STORAGES[storage_scheme](url)
