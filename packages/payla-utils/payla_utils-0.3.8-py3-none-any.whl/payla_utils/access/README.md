## Implement the permission class `DjangoActionPermissions`

```py
from rest_framework import viewsets
from payla_utils.access.permission import DjangoActionPermissions

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoActionPermissions, ]
    permission_base = "users" # if not defined the app label would be used
    queryset = User.objects.all()
    model_class = User # Only required if viewset not using queryset
    # optional perms_map_action to override default behaviour
    perms_map_action = {
        'custom_action': ['users.list_users']
    }
    ...
```

This permission class will check that the `user` calling an action in the viewset has a **Permission** with the `codename` `{app_label}.{action}_{permission_base|app_label}`. In this example, the viewset will raise a 403 error if the user doesn't have a **Permission** with the codename `users.add_users` and tries to call the `create` action (using a POST method). The same applies to the `list`, `retrieve`, `update` and `destroy` actions. Note that PUT and PATCH requests expect the same `users.change_update` **Permission**, event if DRF maps PUT requests with the _partial_update_ action.

For additional actions added to the viewset with the `@action` decorator, the following `codename` convention is expected if you do not want to manually specify it in the view using `perms_map_action`: `{action_name}_{permission_base|app_label}`. For example, if we update the previous viewset to look like this (assuming the app name is `users`):

```py
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoActionPermissions]
    permission_base = "users"
    ...

    @action(methods=['GET', 'POST'])
    def lessons(self, *args, **kwargs):
        ...
```

The permission class will expect the user to have a **Permission** with the codename `users.lessons_users` when a GET or POST request is made.

The `perms_map_action` can also accept a method with the following signature `def method_name(user, view, obj=None)`.

```py

def check_object_permission(user, view, obj=None):
    if not obj:
        return True
    return obj.user.id ==  user.id

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoActionPermissions]
    permission_base = "users"
    perms_map_action = {
        'update': ['users.change_users', check_object_permission]
    }
    ...
```

### Adding new permission

Django automatically creates four basic permissions for every model, these are `add_{modelname}`, `change_{modelname}`, `view_{modelname}` and `delete_{modelname}`. To add new ones, you can define them in the model meta class. see example below

```py
class User(models.Model):
    ...

    class Meta:
        permissions = [
            ("disable_users", "Can be able to disable users"),
            ("activate_users", "Can be able to activate users"),
        ]
```

After defining the permissions, you need to generate a migration using Django command `./manage.py makemigrations`. Make sure to have generated the migration before any other migration that uses this new permission i.e writing a migration to add the new permission to a group.

## Exclude views from a viewset

If you want to exclude a view from the permission checking logic, you can specify the name of the action in the `permission_exclude_views` property. Example:

```py
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoActionPermissions]
    permission_base = "users"
    permission_exclude_views = ['retrieve', 'list', 'lessons']
    ...

    @action(methods=['GET', 'POST'])
    def lessons(self, *args, **kwargs):
        ...

```

## Specific permission_base string for a specific view

If you want to override the `permission_base` for a specific custom action, you can. Example:

```py
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoActionPermissions]
    permission_base = "users"
    ...

    @action(methods=['GET'], permission_base='other_base')
    def lessons(self, *args, **kwargs):
        ...

```

Here, the `lessons_other_base` **Permission** would be expected.
