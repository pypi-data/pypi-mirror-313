# WebCase 2factor API

Package to create general API for 2factor checkers.

## Installation

```sh
pip install wc-django-2factor
```

In `settings.py`:

```python
INSTALLED_APPS += [
    # Dependencies:
    'pxd_admin_extensions',
    'django_jsonform',
    'wcd_settings',

    # 2Factor itself.
    'wcd_2factor',
]

WCD_2FACTOR = {
    # It will be empty by default:
    'METHODS': [
        # Simple builtin 2factor method.
        # Used to work like user secret confirmation.
        # But mostly serves as an example.
        'wcd_2factor.builtins.dummy.DUMMY_METHOD_DESCRIPTOR',
    ],
    # Custom json encoder
    'JSON_ENCODER': 'wcd_2factor.utils.types.EnvoyerJSONEncoder',
}
```

## Usage

### Confirmer

Service for confirmation state management.

```python
from wcd_2factor.confirmer import default_confirmer, Backend, Confirmer
from wcd_2factor.registries import method_config_registry
from wcd_2factor.models import MethodConfig, UserConfig, ConfirmationState

# Default registry

# Use:
default confirmer
# Or create another.
confirmer = Confirmer(method_config_registry)

# List of all available method keys:
default_confirmer.get_methods()

# List of all active `MethodConfig` instances:
default_confirmer.get_method_configs()

# List of all user `UserConfig` configurations:
default_confirmer.get_user_configs(
    # Provide user instance:
    user=user or None,
    # Or identifier:
    user_id=user.pk or None
)


# Creates backend for some method config or `None` if there is no such:
default_confirmer.make_backend(
    # Optional, if `user_config` will be provided, since it also has a
    # relation to a MethodConfig.
    method_config=MethodConfig() or None,
    # Optional, since confirmation could be done just using the MethodConfig 
    # by itself.
    user_config=UserConfig() or None,
    # Optional context to be passed to the backend.
    context={} or None,
    # Whether should raise an exception if backend could not be created.
    # For example when there is no registered method.
    should_raise=False,
)


# Method to change user confirmation.
# Id will check if the changes are significant enough to request a 
# confirmation from user.
# If it does - `make_confirmation` - will be a callable to create new 
# `ConfirmationState` instance. Else `None` will be returned.
instance = UserConfig()
make_confirmation = default_confirmer.change_user_config(
    # Current instance to apply changes to.
    instance,
    # New configuration object. Either a pydantic object or dataclass or just a 
    # simple dict, that will be internally converted to a pydantic object.
    DTO() or dict(),
    # If you already have an initialized backend, method could use it 
    # instead of creating a new one:
    backend=Backend() or None,
    # Optional method config object. If, for example `user_config` instance 
    # doesen't have one attached yet,
    method_config=MethodConfig() or None,
    # Optional context to be passed to the backend's method.
    context={} or None,
)
# Don't forget to save your configuration instance.
# It will not be saved by this method.
instance.save()

if make_confirmation is not None:
    confirmation: ConfirmationState = make_confirmation()

  
# Requesting any type of confirmation:
confirmation: ConfirmationState = default_confirmer.request_confirmation(
    # Optional, if `user_config` will be provided, since it also has a
    # relation to a MethodConfig.
    method_config=MethodConfig() or None,
    # Optional, since confirmation could be done just using the MethodConfig 
    # by itself.
    user_config=UserConfig() or None,
    # If you already have an initialized backend, method could use it 
    # instead of creating a new one:
    backend=Backend() or None,
    # User provided state.
    # It depends on backend what kind of parameters should and should not be 
    # present.
    # In most cases if `used_config` provided - no additional information 
    # required at all.
    state={} or None,
    # Optional context to be passed to the backend's method.
    context={} or None,
)


# If you have user data to confirm some `ConfirmationState` run this:
confirmation: ConfirmationState = default_confirmer.confirm(
    # Either identifier:
    id=uuid4() or None,
    # Or confirmation object itself must be provided:
    confirmation=confirmation or None,
    # User passed data, that confirms that user have control over the 
    # "second factor":
    data={} or None,
    # If you already have an initialized backend, method could use it 
    # instead of creating a new one:
    backend=Backend() or None,
    # Optional context to be passed to the backend's method.
    context={} or None,
)
# Method might return state, event when confirmation process failed for some 
# reason.
# So check the confirmation before using it:
if not confirmation.is_available():
    raise ValueError('Confirmation failed.')


# Checks if confirmation is confirmed and available to use:
available, optional_confirmation = default_confirmer.check(
    # Either identifier:
    id=uuid4() or None,
    # Or confirmation object itself must be provided:
    confirmation=confirmation or None,
    # Optional context to be passed to the backend's method.
    context={} or None,
)
# In some cases method might return None instead of confirmation object.
# That happens when confirmation was already used, or there were none at all.
if not available:
    raise ValueError('Confirmation unavailable.')


# And the last one.
# ConfirmationState object is a "one-time" password to perform some action.
# So after usage it will be deleted from the database.
used, optional_confirmation = default_confirmer.use(
    # Either identifier:
    id=uuid4() or None,
    # Or confirmation object itself must be provided:
    confirmation=confirmation or None,
    # Optional context to be passed to the backend's method.
    context={} or None,
)
# But you will still have object returned if `used` was true.
# You might need to do something with it afterwards.
if not used:
    raise ValueError('Confirmation failed.')
```

### Registry and custom Backends

Registry is a simple dict with some additional methods to register new confirmation methods.

For every method that could be used in your application `MethodConfigDescriptor` should be defined and added to registry.

For example:

```python
from wcd_2factor.registries import (
    method_config_registry, Registry,
    MethodConfigDescriptor, DTO,
)

# This is a default method's registry. 
# It will be autopopulated with descriptors from 
# django_settings.WCD_2FACTOR['METHODS'].
method_config_registry

# But nothing stops you from creating your own registry.
my_registry = Registry()

# And after that you may add descriptors to it.
MY_METHOD_DESCRIPTOR = my_registry.register(MethodConfigDescriptor(
    # Unique method key.
    key='my_method',
    # Verbose method name.
    verbose_name=gettext_lazy('My Method'),
    # Backend class is required, since it will be used to execute every
    # `Confirmer` method.
    backend_class=Backend,
    # Other data object classes and schemas are optional:
    # MethodConfig pydantic class.
    # Configuration model for MethodConfig.
    config_global_dto=BaseModel or None,
    # JSONSchema for that configuration.
    config_global_schema=BaseModel.model_json_schema() or None,
    # Configuration model for UserConfig.
    config_user_dto=BaseModel or None,
    # JSONSchema for that configuration.
    config_user_schema=BaseModel.model_json_schema() or None,
))
```

But descriptor is only a simple definition with and additional configuration inside.

All the work with message sending and request confirmation are on your `Backend` implementation.

```python
from wcd_2factor.confirmer import Backend
from wcd_2factor.registries import DTO, MethodConfigDescriptor
from wcd_2factor.models import ConfirmationState, UserConfig


class YourBackend(Backend):
    method_config: YourMethodDTO
    user_config: Optional[YourUserDTO]

    # Method that checks if user configuration changed.
    # And if this change is significant enough to request a confirmation.
    def change_user_config(
        self,
        # New configuration to check for changes.
        new: YourMethodDTO,
        context: Optional[dict] = None,
    ) -> Tuple[bool, Optional[dict]]:
        # Pseudocode:

        if (
            self.user_config is None
            or
            self.user_config != new
        ):
            # Then user configuration changed and confirmation with
            # some "state" should be created to confirm the change.
            return True, {'some': 'state'}

        # Otherwise - do nothing.
        return False, None

    # This is method for all confirmation requests creation.
    # Whether it's for user confirmation or not, with empty `self.user_config` 
    # and only `self.method_config` available or "fully configured"".
    def request_confirmation(
        self,
        # User or application provided state.
        state: dict,
        context: Optional[dict] = None,
    ) -> Tuple[ConfirmationState.Status, dict]:
        return ConfirmationState.Status.IN_PROCESS, {
            **state,
            'some_confirmation_token_to_check': 'value',
        }

    # To confirm saved confirmation state, `Confirmer` will call this method.
    def confirm(
        self,
        # State from `ConfirmationState` object.
        state: dict,
        # User-provided data to validate against.
        user_data: Any,
        context: Optional[dict] = None,
    ) -> bool:
        # Return True if user provided something that is somehow valid 
        # against the stored state.
        # User will never have access to the ConfigurationState data from 
        # your `request_confirmation` object.
        # At least he should not.
        return (
            state.get('some_confirmation_token_to_check')
            ==
            user_data.get('validation_token')
        )
```

### Frontend/DRF

Library has an API implmentation based on DjangoRestFramework.

It is available in `wcd_2factor.contrib.dtf` module.

In `urls.py`:

```python
from wcd_2factor.contrib.drf.views import make_urlpatterns as twofactor_make_urlpatterns


urlpatters = [
  # ...
  path(
    'api/v1/auth/2factor/',
    include(
      (twofactor_make_urlpatterns(), 'wcd_2factor'),
      namespace='2factor',
    )
  ),
]
```

And after the `/api/v1/auth/2factor/` you will have several endpoints:

#### Method configurations

**GET:** `method-config/list/active/` - List of active method configs.

#### User configurations

**GET:** `user-config/own/list/` - List of user's configurations.

**POST:** `user-config/own/create/` - Creating a new user configuration.
```json
{
  // Selected global method config.
  "method_config_id": 1,
  // Configuration data. 
  "config": {"email": "ad@ad.com"},
  // 2Factor method could be deactivated by user.
  "is_active": false,
  // Setting some method as a default.
  "is_default": false,
}
```

**POST:** `user-config/own/confirm/` - Confirming unconfirmed user configuration.
```json
{
  // User config id.
  "id": 1,
  // Unconfirmed confirmation identifier.
  "confirmation_id": "uuid-confirmation-identifier-0000",
  // Data to confirm with.
  "data": {"code": "some"},
}
```

**PUT:** `user-config/own/<int:pk>/update/` - Updating user configuration.
```json
{
  // Configuration data. 
  "config": {"email": "ad@ad.com"},
  // 2Factor method could be deactivated by user.
  "is_active": false,
  // Setting some method as a default.
  "is_default": false,
}
```

**DELETE:** `user-config/own/<int:pk>/destroy/` - Deletes user configuration.

#### Confirmation

**POST:** `confirmation/request/` - Creating a new confirmation.
```json
{
  // One of `method_config_id` or `user_config_id` must be provided:
  // Selected global method config. For example if user doesn't have it's own.
  "method_config_id": 1,
  // Selected user configuration method.
  "user_config_id": 1,
  // Additional data, if required. For example an "email" to confirm.
  "data": {"some": "data"},
}
```

Result will have a confirmation identifier. So on the frontend side it should be saved to confirm later.

**GET:** `confirmation/{confirmation_id}/check/` - Will return current `ConfirmationState` status.

**POST:** `confirmation/confirm/` - Method to confirm previously created "request".
```json
{
  // ConfirmationState identifier.
  "id": "uuid-confirmation-identifier-0000",
  // User data, that backend will use to validate the confirmation.
  "data": {"code": "confirmation-000-code"},
}
```

It will return the same data as previous requests, but this time confirmation `status` will be `confirmed`, or not if confirmation failed.
