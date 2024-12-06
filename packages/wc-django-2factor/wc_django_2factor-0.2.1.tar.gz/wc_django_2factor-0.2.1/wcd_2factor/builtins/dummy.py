from typing import *

from wcd_2factor.confirmer import Backend
from wcd_2factor.registries import DTO, MethodConfigDescriptor
from wcd_2factor.models import ConfirmationState, UserConfig


class DummyMethodDTO(DTO):
    code: str = 'dummy-method'


class DummyUserDTO(DTO):
    code: str


class DummyBackend(Backend):
    method_config: DummyMethodDTO
    user_config: Optional[DummyUserDTO]

    def change_user_config(
        self,
        new: DummyUserDTO,
        context: Optional[dict] = None,
    ) -> Tuple[bool, Optional[dict]]:
        old = self.user_config
        new = new.model_copy()
        self.user_config = new

        assert new.code is not None and new.code, (
            'Code must not be empty when configuring user.'
        )

        if old is not None and new.code == old.code:
            return False, None

        return True, {'code': new.code}

    def request_confirmation(
        self,
        state: dict,
        context: Optional[dict] = None,
    ) -> Tuple[ConfirmationState.Status, dict]:
        return ConfirmationState.Status.IN_PROCESS, {
            **state,
            'code': (
                self.user_config.code
                if self.user_config is not None else
                self.method_config.code
            ),
        }

    def confirm(
        self,
        state: dict,
        user_data: Any,
        context: Optional[dict] = None,
    ) -> bool:
        state_code = state.get('code')

        if state_code == user_data.get('code') and state_code:
            return True

        return False


DUMMY_METHOD_DESCRIPTOR = MethodConfigDescriptor(
    key='dummy',
    backend_class=DummyBackend,
    config_global_dto=DummyMethodDTO,
    config_global_schema=DummyMethodDTO.model_json_schema(),
    config_user_dto=DummyUserDTO,
    config_user_schema=DummyUserDTO.model_json_schema(),
)
