import json
from pathlib import Path

from synapse_sdk.plugins.categories.registry import _REGISTERED_ACTIONS, register_actions
from synapse_sdk.plugins.enums import PluginCategory
from synapse_sdk.utils.file import get_dict_from_file


def get_action(action, params_data, *args, **kwargs):
    if isinstance(params_data, str):
        try:
            params = json.loads(params_data)
        except json.JSONDecodeError:
            params = get_dict_from_file(params_data)
    else:
        params = params_data

    config_data = kwargs.pop('config', False)
    if config_data:
        if isinstance(config_data, str):
            config = read_plugin_config(plugin_path=config_data)
        else:
            config = config_data
    else:
        config = read_plugin_config()
    category = config['category']
    return get_action_class(category, action)(params, config, *args, **kwargs)


def get_action_class(category, action):
    register_actions()
    return _REGISTERED_ACTIONS[category][action]


def get_available_actions(category):
    register_actions()
    return list(_REGISTERED_ACTIONS[category].keys())


def get_plugin_categories():
    return [plugin_category.value for plugin_category in PluginCategory]


def read_plugin_config(plugin_path=None):
    config_file_name = 'config.yaml'
    if plugin_path:
        config_path = Path(plugin_path) / config_file_name
    else:
        config_path = config_file_name
    return get_dict_from_file(config_path)
