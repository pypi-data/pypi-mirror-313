from ray import serve

from synapse_sdk.clients.exceptions import ClientError
from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class DeploymentAction(Action):
    name = 'deployment'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.JOB

    def get_deployment(self):
        return serve.deployment(ray_actor_options=self.get_actor_options())(self.entrypoint)

    def get_actor_options(self):
        return {'runtime_env': self.get_runtime_env()}

    def start(self):
        deployment = self.get_deployment()
        serve.delete(self.plugin_release.code)
        # TODO add run object
        serve.run(deployment.bind(), name=self.plugin_release.code, route_prefix=f'/{self.plugin_release.checksum}')

        # 백엔드에 ServeApplication 추가
        serve_application = self.create_serve_application()
        return {'serve_application': serve_application['id'] if serve_application else None}

    def create_serve_application(self):
        if self.client:
            try:
                job = self.client.get_job(self.job_id)
                serve_application = self.ray_client.get_serve_application(self.plugin_release.code)
                return self.client.create_serve_application({
                    'plugin': self.plugin_release.plugin,
                    'version': self.plugin_release.version,
                    'agent': job['agent'],
                    'status': serve_application['status'],
                    'data': serve_application,
                })
            except ClientError:
                pass
        return None
