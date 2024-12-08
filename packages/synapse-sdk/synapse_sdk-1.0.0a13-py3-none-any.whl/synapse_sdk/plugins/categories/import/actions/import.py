from synapse_sdk.plugins.categories.base import Action
from synapse_sdk.plugins.categories.decorators import register_action
from synapse_sdk.plugins.enums import PluginCategory, RunMethod


@register_action
class ImportAction(Action):
    name = 'import'
    category = PluginCategory.IMPORT
    method = RunMethod.JOB
