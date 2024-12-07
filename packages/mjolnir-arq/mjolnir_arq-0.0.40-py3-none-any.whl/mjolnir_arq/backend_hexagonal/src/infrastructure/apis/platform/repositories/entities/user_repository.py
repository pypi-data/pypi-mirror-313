from typing import Dict, Union
from src.core.classes.api_client import ApiClient
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.apis.platform.entities.user.index import (
    UserDelete,
    UserRead,
    UserUpdate,
    UserSave,
)
from src.domain.services.repositories.apis.platform.entities.i_user_repository import (
    IUserRepository,
)

class UserRepository(IUserRepository):
    base_url = settings.api_platform

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def save(self, config: Config, params: UserSave) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    def update(self, config: Config, params: UserUpdate) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    def list(self, config: Config, params: Pagination) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    def delete(
        self,
        config: Config,
        params: UserDelete,
    ) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def read(
        self,
        config: Config,
        params: UserRead,
    ) -> Union[Dict, None]:
        api_client = ApiClient(base_url=self.base_url, config=config)
        endpoint = f"/user/{params.id}"
        user_data = await api_client.get(endpoint)
        return user_data
