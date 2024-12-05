import os
from typing import Any

from admin_interface.cache import del_cached_active_theme
from admin_interface.models import Theme
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from payla_utils.settings import payla_utils_settings


class Command(BaseCommand):
    """
    This management command will init environment based on the current env (local.dev, dev, stage, playground and prod)

    - load fixtures on the first run (when the DB is empty)
    - setup custom theme for admin_interface
    - create user when not in prod if `LOCAL_DJANGO_ADMIN_PASSWORD` is set

    APP_NAME and ENVIRONMENT settings are required.
    """

    def add_arguments(self, parser):
        parser.add_argument('--env', type=str, default='', help='force which env to use')

    def handle(self, *args: Any, **options: Any):
        env = options.get('env') or payla_utils_settings.ENVIRONMENT
        self.setup_theme(env)
        self.setup_initial_fixtures(env=env)
        self.run_extra_commands()

    def setup_initial_fixtures(self, env: str) -> None:
        if not get_user_model().objects.all().exists():
            for fixture in payla_utils_settings.INITIAL_FIXTURES:
                call_command('loaddata', fixture)
            if not env.lower().startswith('prod') and payla_utils_settings.LOCAL_DJANGO_ADMIN_PASSWORD:
                # password has to be handed over as an environment variable
                os.environ.setdefault('DJANGO_SUPERUSER_PASSWORD', payla_utils_settings.LOCAL_DJANGO_ADMIN_PASSWORD)
                call_command('createsuperuser', '--username', 'admin', '--email', 'tools@payla.de', '--noinput')
        else:
            self.stdout.write(
                self.style.WARNING("Not importing fixtures as there seems to be data present. Please check.")
            )

    def setup_theme(self, env: str) -> None:
        base_title = payla_utils_settings.APP_NAME
        theme_settings = {
            'css_module_rounded_corners': True,
            'env_name': env.upper(),
            'title': f'{base_title} ({env.upper()})',
        }
        env_themes = payla_utils_settings.ENV_THEMES

        if env.lower() not in env_themes:
            self.stdout.write(
                self.style.WARNING(f'No theme settings for env {env.lower()} found. Skipping theme setup.')
            )
            return

        theme: Theme = Theme.objects.get_active()
        theme_settings.update(env_themes[env.lower()])
        # update theme name if set to APP_NAME key
        if theme_settings['title'] == 'APP_NAME':
            theme_settings['title'] = base_title
        for field_name, field_value in theme_settings.items():
            setattr(theme, field_name, field_value)
        theme.save()
        del_cached_active_theme()

    def run_extra_commands(self):
        for command in payla_utils_settings.RUN_EXTRA_COMMANDS:
            custom_command = command.split(' ')
            # handle custom commands with arguments
            if len(custom_command) > 1:
                new_command, *args = custom_command
                call_command(new_command, *args)
            else:
                call_command(command)
