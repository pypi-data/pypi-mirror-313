import hashlib
import json
import operator
import zipfile
from functools import reduce
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml


def download_file(url, path_download, name=None, coerce=None):
    if name:
        name += Path(url).suffix
    else:
        name = Path(url).name

    name = urlparse(name).path
    path = Path(path_download) / name
    if not path.is_file():
        r = requests.get(url, allow_redirects=True)
        open(str(path), 'wb').write(r.content)

    if coerce:
        path = coerce(path)

    return path


def files_url_to_path(files, coerce=None):
    path_download = Path('/tmp/datamaker') / 'media'
    path_download.mkdir(parents=True, exist_ok=True)
    for file_name in files:
        if isinstance(files[file_name], str):
            files[file_name] = download_file(files[file_name], path_download, coerce=coerce)
        else:
            files[file_name]['path'] = download_file(files[file_name].pop('url'), path_download, coerce=coerce)


def files_url_to_path_from_objs(objs, files_fields, coerce=None, is_list=False):
    if not is_list:
        objs = [objs]

    for obj in objs:
        for files_field in files_fields:
            try:
                files = reduce(operator.getitem, files_field.split('.'), obj)
                files_url_to_path(files, coerce=coerce)
            except KeyError:
                pass


def get_dict_from_file(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)

    with open(file_path) as f:
        if file_path.suffix == '.yaml':
            return yaml.safe_load(f)
        else:
            return json.load(f)


def calculate_checksum(file_path, prefix=''):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            md5_hash.update(byte_block)
    checksum = md5_hash.hexdigest()
    if prefix:
        return f'dev-{checksum}'
    return checksum


def archive(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)

    with zipfile.ZipFile(output_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
        if input_path.is_file():
            zipf.write(input_path, input_path.name)
        else:
            for file_path in input_path.rglob('*'):
                if file_path.is_file():  # Only add files, skip directories
                    arcname = file_path.relative_to(input_path.parent)
                    zipf.write(file_path, arcname)
