"""
Settings for Payla Utils are all namespaced in the PAYLA_UTILS setting.
For example your project's `settings.py` file might look like this:
PAYLA_UTILS = {
    'APP_NAME': 'My App',
    # Used for json logging
    'MICROSERVICE_NAME: 'myapp',
    # dev, stage, prod ...
    'ENVIRONMENT': ENVIRONMENT,
    'INITIAL_FIXTURES': [
        os.path.join(BASE_DIR, 'testapp', 'fixtures', 'users.json'),
    ],
    'SERVER_IP': '192.168.1.4',
    'REQUEST_ID_HEADER': 'X-Request-ID',
    'RUN_EXTRA_COMMANDS': ['loadinitialusers', 'setup_something'],
    'LOCAL_DJANGO_ADMIN_PASSWORD': os.environ.get('LOCAL_DJANGO_ADMIN_PASSWORD', 'admin'),
    'USE_PGTRIGGER': False,
    'USE_HISTORICAL_MODELS': False,
    'HISTORICAL_IGNORE_FIELD_NAME': [],
    'ENV_THEMES': {
        'local.dev': {
            'title_color': '#000000',
            'css_header_background_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_text_color': '#000000',
            'css_header_link_color': '#000000',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#ababab',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#000000',
            'css_module_link_color': '#000000',
            'css_module_link_hover_color': '#3255fe',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#6d6d6d',
            'css_save_button_background_hover_color': '#4a4a4a',
        },
        'dev': {
            'title_color': '#ffffff',
            'env_color': '#00cb68',
            'css_header_background_color': '#007b3b',
            'css_header_text_color': '#f5dd5d',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#006731',
            'css_module_background_selected_color': '#ffffff',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#5f0000',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#006731',
            'css_save_button_background_hover_color': '#01a74f',
        },
        'stage': {
            'title_color': '#ffffff',
            'env_color': '#ffcb38',
            'css_header_background_color': '#ff9722',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#41aad1',
            'css_module_background_color': '#ca6a00',
            'css_module_background_selected_color': '#ffffff',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#41aad1',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#ca6a00',
            'css_save_button_background_hover_color': '#ff9722',
        },
        'playground': {
            'title_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_background_color': '#09137a',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#0020bf',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#69c2cc',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#0038ff',
            'css_save_button_background_hover_color': '#02208b',
        },
        'prod': {
            'title_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_background_color': '#720606',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#e73f41',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#5f0000',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#720606',
            'css_save_button_background_hover_color': '#4a4a4a',
            # APP_NAME will be replaced by the correct app name set in payla utils settings
            'title': 'APP_NAME',
        },
    }
}
This module provides the `payla_utils_setting` object, that is used to access
Payla Utils settings, checking for user settings first, then falling
back to the defaults.
"""

from __future__ import annotations

from django.conf import settings

# Import from `django.core.signals` instead of the official location
# `django.test.signals` to avoid importing the test module unnecessarily.
from django.core.signals import setting_changed

DEFAULTS: dict = {
    'APP_NAME': None,
    'MICROSERVICE_NAME': None,
    'ENVIRONMENT': None,
    'INITIAL_FIXTURES': [],
    'RUN_EXTRA_COMMANDS': [],
    'LOCAL_DJANGO_ADMIN_PASSWORD': None,
    'REQUEST_ID_HEADER': None,
    'SERVER_IP': None,
    'USE_PGTRIGGER': False,
    'USE_HISTORICAL_MODELS': False,
    'HISTORICAL_IGNORE_MODELS': [],
    'HISTORICAL_IGNORE_FIELD_NAME': [],
    'GROUPS_PERMISSIONS_FILE_PATH': None,
    'ENV_THEMES': {
        'local.dev': {
            'title_color': '#000000',
            'css_header_background_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_text_color': '#000000',
            'css_header_link_color': '#000000',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#ababab',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#000000',
            'css_module_link_color': '#000000',
            'css_module_link_hover_color': '#3255fe',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#6d6d6d',
            'css_save_button_background_hover_color': '#4a4a4a',
        },
        'dev': {
            'title_color': '#ffffff',
            'env_color': '#00cb68',
            'css_header_background_color': '#007b3b',
            'css_header_text_color': '#f5dd5d',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#006731',
            'css_module_background_selected_color': '#ffffff',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#5f0000',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#006731',
            'css_save_button_background_hover_color': '#01a74f',
        },
        'stage': {
            'title_color': '#ffffff',
            'env_color': '#ffcb38',
            'css_header_background_color': '#ff9722',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#41aad1',
            'css_module_background_color': '#ca6a00',
            'css_module_background_selected_color': '#ffffff',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#41aad1',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#ca6a00',
            'css_save_button_background_hover_color': '#ff9722',
        },
        'playground': {
            'title_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_background_color': '#09137a',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#0020bf',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#69c2cc',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#0038ff',
            'css_save_button_background_hover_color': '#02208b',
        },
        'prod': {
            'title_color': '#ffffff',
            'env_color': '#00cb38',
            'css_header_background_color': '#720606',
            'css_header_text_color': '#ffffff',
            'css_header_link_color': '#ffffff',
            'css_header_link_hover_color': '#1e00ac',
            'css_module_background_color': '#e73f41',
            'css_module_background_selected_color': '#e3e3e3',
            'css_module_text_color': '#ffffff',
            'css_module_link_color': '#ffffff',
            'css_module_link_hover_color': '#5f0000',
            'css_generic_link_color': '#000000',
            'css_save_button_background_color': '#720606',
            'css_save_button_background_hover_color': '#4a4a4a',
            'title': 'APP_NAME',
        },
    },
}


class PaylaUtilsSettings:
    def __init__(self, defaults: dict | None = None) -> None:
        self.defaults = defaults or DEFAULTS
        self._cached_attrs: set = set()

    @property
    def user_settings(self) -> dict:
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'PAYLA_UTILS', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid setting: '{attr}'")

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self) -> None:
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


payla_utils_settings = PaylaUtilsSettings(DEFAULTS)


def reload_payla_utils_settings(*args, **kwargs) -> None:
    setting = kwargs['setting']
    if setting == 'PAYLA_UTILS':
        payla_utils_settings.reload()


setting_changed.connect(reload_payla_utils_settings)
