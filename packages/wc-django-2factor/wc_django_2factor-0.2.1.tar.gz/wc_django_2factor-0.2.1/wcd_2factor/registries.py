from typing import *
import logging
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from wcd_settings.utils.descriptor_registry import (
    DescriptorRegistry, Descriptor,
)
if TYPE_CHECKING:
    from wcd_2factor.confirmer.backends import Backend


__all__ = (
    'DTO',
    'MethodConfigDescriptor',
    'Registry',
    'method_config_registry',
)

logger = logging.getLogger(__name__)


class DTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        extra='allow',
    )


CD = TypeVar('CD', bound=DTO)
UD = TypeVar('UD', bound=DTO)


class MethodConfigDescriptor(Generic[CD, UD], Descriptor):
    backend_class: Type['Backend']
    config_global_dto: Optional[Type[CD]] = None
    config_global_schema: Optional[dict] = None
    config_user_dto: Optional[Type[UD]] = None
    config_user_schema: Optional[dict] = None


class Registry(DescriptorRegistry):
    pass


method_config_registry = Registry()
