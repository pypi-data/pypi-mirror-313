from synapse_sdk.clients.base import BaseClient
from synapse_sdk.clients.exceptions import ClientError


class RayClientMixin(BaseClient):
    def get_job(self, pk):
        path = f'jobs/{pk}/'
        return self._get(path)

    def list_jobs(self):
        path = 'jobs/'
        return self._get(path)

    def list_job_logs(self, pk):
        path = f'jobs/{pk}/logs/'
        return self._get(path)

    def tail_job_logs(self, pk):
        if self.long_poll_handler:
            raise ClientError(400, '"tail_job_logs" does not support long polling')

        path = f'jobs/{pk}/tail_logs/'

        url = self._get_url(path)
        headers = self._get_headers()

        response = self.requests_session.get(url, headers=headers, stream=True)
        for line in response.iter_lines(decode_unicode=True):
            if line:
                yield f'{line}\n'

    def get_node(self, pk):
        path = f'nodes/{pk}/'
        return self._get(path)

    def list_nodes(self):
        path = 'nodes/'
        return self._get(path)

    def get_task(self, pk):
        path = f'tasks/{pk}/'
        return self._get(path)

    def list_tasks(self):
        path = 'tasks/'
        return self._get(path)

    def get_serve_application(self, pk):
        path = f'serve_applications/{pk}/'
        return self._get(path)

    def list_serve_applications(self):
        path = 'serve_applications/'
        return self._get(path)

    def delete_serve_application(self, pk):
        path = f'serve_applications/{pk}/'
        return self._delete(path)
