from synapse_sdk.clients.backend.annotation import AnnotationClientMixin
from synapse_sdk.clients.backend.dataset import DatasetClientMixin
from synapse_sdk.clients.backend.integration import IntegrationClientMixin
from synapse_sdk.clients.backend.ml import MLClientMixin


class BackendClient(AnnotationClientMixin, DatasetClientMixin, IntegrationClientMixin, MLClientMixin):
    name = 'Backend'
    token = None
    tenant = None

    def __init__(self, base_url, token=None, tenant=None):
        super().__init__(base_url)
        self.token = token
        self.tenant = tenant

    def _get_headers(self):
        headers = {}
        if self.token:
            headers = {'Authorization': f'Token {self.token}'}
        if self.tenant:
            headers['SYNAPSE-Tenant'] = f'Token {self.tenant}'
        return headers
