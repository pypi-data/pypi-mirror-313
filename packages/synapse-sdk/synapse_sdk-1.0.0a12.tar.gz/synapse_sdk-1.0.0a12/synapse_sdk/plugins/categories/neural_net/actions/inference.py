from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class InferenceAction(Action):
    name = 'inference'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.RESTAPI

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        headers = {'serve_multiplexed_model_id': str(self.params.pop('model'))}
        if 'headers' in self.params:
            self.params['headers'].update(headers)
        else:
            self.params['headers'] = headers
