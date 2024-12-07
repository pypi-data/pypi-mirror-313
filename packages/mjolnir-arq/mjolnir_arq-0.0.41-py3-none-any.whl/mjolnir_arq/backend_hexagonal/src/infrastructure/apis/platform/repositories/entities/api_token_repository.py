from typing import  Dict, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.classes.api_client import ApiClient
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.apis.platform.entities.api_token.api_token_read import ApiTokenRead
from src.domain.models.apis.platform.entities.api_token.api_token_save import ApiTokenSave
from src.domain.models.apis.platform.entities.api_token.api_token_update import ApiTokenUpdate
from src.domain.models.apis.platform.entities.api_token.api_token_delete import ApiTokenDelete
from src.domain.services.repositories.apis.platform.entities.i_api_token_repository import IApiTokenRepository


class ApiTokenRepository(IApiTokenRepository):
    base_url = settings.api_platform
    base_pipe = "/api-token/"

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def save(self, config: Config, params: ApiTokenSave) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def update(self, config: Config, params: ApiTokenUpdate) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def list(self, config: Config, params: Pagination) -> Union[Dict, None]:
        api_client = ApiClient(base_url=self.base_url, config=config)
        endpoint = f"{self.base_pipe}list"
        data = await api_client.post(endpoint, data=params)
        return data
        

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def delete(
        self,
        config: Config,
        params: ApiTokenDelete,
    ) -> Union[Dict, None]:
        pass

    @execute_transaction(layer=LAYER.I_A_P_R_E.value, enabled=settings.has_track)
    async def read(
        self,
        config: Config,
        params: ApiTokenRead,
    ) -> Union[Dict, None]:
        api_client = ApiClient(base_url=self.base_url, config=config)
        endpoint = f"{self.base_pipe}{params.id}"
        data = await api_client.get(endpoint)
        return data
        