from synapse_sdk.clients.base import BaseClient
from synapse_sdk.clients.utils import get_default_url_conversion


class MLClientMixin(BaseClient):
    def list_models(self, params=None):
        path = 'models/'
        return self._get(path, params=params)

    def get_model(self, pk, params=None, url_conversion=None):
        path = f'models/{pk}/'
        url_conversion = get_default_url_conversion(
            url_conversion, files_fields=['files', 'parent.files'], is_list=False
        )
        return self._get(path, params=params, url_conversion=url_conversion)

    def create_model(self, data):
        path = 'models/'
        files = {'file': data.pop('file')}
        return self._post(path, data=data, files=files)

    def create_serve_application(self, data):
        path = 'serve_applications/'
        return self._post(path, data=data)

    def list_ground_truth_events(self, params=None, url_conversion=None, list_all=False):
        path = 'ground_truth_events/'
        url_conversion = get_default_url_conversion(url_conversion, files_fields=['files'])
        return self._list(path, params=params, url_conversion=url_conversion, list_all=list_all)
