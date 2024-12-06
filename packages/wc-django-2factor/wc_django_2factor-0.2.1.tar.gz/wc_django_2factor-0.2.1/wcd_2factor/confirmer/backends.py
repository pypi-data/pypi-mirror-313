from typing import *

from wcd_2factor.registries import DTO
from wcd_2factor.models import ConfirmationState, UserConfig

if TYPE_CHECKING:
    from .confirmer import Confirmer


__all__ = 'Backend',

D = TypeVar('D', bound=DTO)


class Backend:
    def __init__(
        self,
        *,
        method_config: DTO,
        user_config: Optional[DTO] = None,
        confirmer: Optional['Confirmer'] = None,
        context: Optional[dict] = None
    ):
        self.context = context if context is not None else {}
        self.confirmer = confirmer
        self.method_config = method_config
        self.user_config = user_config

        self.configure()

    def from_context(self, prop: Hashable, context: Optional[dict] = None):
        value = None

        if context is not None and prop in context:
            value = context[prop]

        if value is None:
            value = self.context.get(prop)

        return value

    def configure(self):
        pass

    def change_user_config(
        self,
        new: DTO,
        context: Optional[dict] = None,
    ) -> Tuple[bool, Optional[dict]]:
        raise NotImplementedError()

    def request_confirmation(
        self,
        state: dict,
        context: Optional[dict] = None,
    ) -> Tuple[ConfirmationState.Status, dict]:
        raise NotImplementedError()

    def confirm(
        self,
        state: dict,
        user_data: Any,
        context: Optional[dict] = None,
    ) -> bool:
        raise NotImplementedError()
