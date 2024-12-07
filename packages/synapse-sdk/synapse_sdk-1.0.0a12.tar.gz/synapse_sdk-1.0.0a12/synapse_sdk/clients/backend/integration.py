from synapse_sdk.clients.base import BaseClient


class IntegrationClientMixin(BaseClient):
    def health_check_agent(self, token):
        path = f'agents/{token}/connect/'
        return self._post(path)

    def get_plugin(self, pk):
        path = f'plugins/{pk}/'
        return self._get(path)

    def create_plugin(self, data):
        path = 'plugins/'
        return self._post(path, data=data)

    def update_plugin(self, pk, data):
        path = f'plugins/{pk}/'
        return self._put(path, data=data)

    def run_plugin(self, pk, data):
        path = f'plugins/{pk}/run/'
        return self._post(path, data=data)

    def get_plugin_release(self, pk, params=None):
        path = f'plugin_releases/{pk}/'
        return self._get(path, params=params)

    def create_plugin_release(self, data):
        path = 'plugin_releases/'
        files = {'file': data.pop('file')}
        return self._post(path, data=data, files=files)

    def get_job(self, pk, params=None):
        path = f'jobs/{pk}/'
        return self._get(path, params=params)

    def list_jobs(self, params=None):
        path = 'jobs/'
        return self._get(path, params=params)

    def update_job(self, pk, data):
        path = f'jobs/{pk}/'
        return self._patch(path, data=data)

    def list_job_console_logs(self, pk):
        path = f'jobs/{pk}/console_logs/'
        return self._get(path)

    def tail_job_console_logs(self, pk):
        path = f'jobs/{pk}/tail_console_logs/'

        url = self._get_url(path)
        headers = self._get_headers()

        response = self.requests_session.get(url, headers=headers, stream=True)
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield f'{line}\n'

    def create_logs(self, data):
        path = 'logs/'
        return self._post(path, data=data)
