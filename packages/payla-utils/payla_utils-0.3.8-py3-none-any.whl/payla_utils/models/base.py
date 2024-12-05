from __future__ import annotations

import contextlib
from functools import lru_cache
from typing import Any

import pgtrigger
from django.conf import settings
from django.contrib.admin.sites import all_sites
from django.core.checks import Error
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from payla_utils.settings import payla_utils_settings


class PaylaQuerySet(models.QuerySet):
    """
    This custom QuerySet with get_or_none method
    """

    def get_or_none(self, *args: Any, **kwargs: Any) -> PaylaModel | None:
        """
        Use this instead of Queryset.get to either get an object if it exists or
        None if it doesn't. This is a shortcut to avoid having to catch DoesNotExist
        exceptions.

        Returns:
            PaylaModel | None: Either the model if it exists or None if it doesn't.
        """
        try:
            return self.get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None

    def update(self, *args, **kwargs) -> int:
        """
        Override Queryset.update to make sure that modified_at is also updated when
        performing multi-row updates.

        Returns:
            int: number of rows updated
        """
        if 'modified_at' not in kwargs:
            kwargs['modified_at'] = now()
        return super().update(*args, **kwargs)


class PaylaModelMeta(models.base.ModelBase):
    """
    Metaclass for PaylaModel
    """

    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if payla_utils_settings.USE_PGTRIGGER and not new_class._meta.abstract:
            pgtrigger.register(
                pgtrigger.Trigger(
                    name='update_modified_at',
                    operation=pgtrigger.Update,
                    # Trigger BEFORE updates
                    when=pgtrigger.Before,
                    # Update modified_at field to current time
                    func="NEW.modified_at = clock_timestamp();RETURN NEW;",
                    # Trigger only if something changed in the row, but not the modified_at field
                    condition=pgtrigger.Condition(
                        'OLD.* IS DISTINCT FROM NEW.* AND OLD.modified_at IS NOT DISTINCT FROM NEW.modified_at'
                    ),
                )
            )(new_class)

        if payla_utils_settings.USE_HISTORICAL_MODELS:
            try:
                from simple_history import register
                from simple_history.exceptions import MultipleRegistrationsError
            except ImportError as exc:
                raise ImportError(
                    'simple_history must be installed in order to use PaylaModel with USE_HISTORICAL_MODELS=True'
                ) from exc

            records_config = {
                'inherit': True,
            }
            is_abstract = getattr(new_class._meta, 'abstract', False)
            is_proxy = getattr(new_class._meta, 'proxy', False)
            ignore = new_class._meta.label in payla_utils_settings.HISTORICAL_IGNORE_MODELS
            if not is_abstract and not is_proxy and not ignore:
                # only register historical models for subclasses of PaylaModel

                # exclude globally ignored fields: e.g api_id ...
                for field_to_exclude in payla_utils_settings.HISTORICAL_IGNORE_FIELD_NAME:
                    if field_to_exclude in new_class.__dict__:
                        records_config.setdefault('excluded_fields', []).append(field_to_exclude)

                with contextlib.suppress(MultipleRegistrationsError):
                    register(new_class, **records_config)

        return new_class


class PaylaModel(models.Model, metaclass=PaylaModelMeta):
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=_('Last modified'), auto_now=True)

    objects = PaylaQuerySet.as_manager()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['modified_at']),
        ]

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        modified field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get('update_fields')
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'modified_at'})

        super().save(*args, **kwargs)

    @classmethod
    @lru_cache(maxsize=1)
    def get_registered_models(cls) -> set[models.Model]:
        registered_models = set()
        for admin_site in all_sites:
            for model, admin in admin_site._registry.items():
                registered_models.add(model)
                for inline in admin.inlines:
                    registered_models.add(inline.model)
        return registered_models

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        if hasattr(cls, 'objects') and not issubclass(cls.objects._queryset_class, PaylaQuerySet):
            errors.append(
                Error(
                    f'Model {cls.__name__} objects must be a subclass of PaylaQuerySet',
                    hint=f'Your custom queryset class for model {cls.__name__} must be extending from PaylaQueryset',
                    obj=cls,
                    id='payla_utils.E001',
                )
            )

        if cls not in cls.get_registered_models():
            errors.append(
                Error(
                    f"Model {cls.__name__} does not have an admin",
                    hint=f"Register the model {cls.__name__} in the admin",
                    obj=cls,
                    id='payla_utils.E002',
                )
            )

        for field in cls._meta.get_fields():
            if field.concrete and (field.null and not field.blank):
                errors.append(
                    Error(
                        f"Field {field.name} of model {cls.__name__} is nullable but not blank",
                        hint=f"Either make field {field.name} non-nullable or blank",
                        obj=cls,
                        id='payla_utils.E003',
                    )
                )

        if payla_utils_settings.USE_PGTRIGGER and 'pgtrigger' not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    'pgtrigger must be installed in order to use PaylaModel with USE_PGTRIGGER=True',
                    hint='Add pgtrigger to INSTALLED_APPS',
                    obj=cls,
                    id='payla_utils.E004',
                )
            )

        if payla_utils_settings.USE_HISTORICAL_MODELS and 'simple_history' not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    'simple_history must be installed in order to use PaylaModel with USE_HISTORICAL_MODELS=True',
                    hint='Add simple_history to INSTALLED_APPS',
                    obj=cls,
                    id='payla_utils.E005',
                )
            )

        return errors
