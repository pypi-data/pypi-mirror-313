
from typing import Dict, Union
from abc import ABC, abstractmethod

from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.apis.platform.entities.api_token.api_token import ApiToken
from src.domain.models.apis.platform.entities.api_token.api_token_read import ApiTokenRead
from src.domain.models.apis.platform.entities.api_token.api_token_update import ApiTokenUpdate
from src.domain.models.apis.platform.entities.api_token.api_token_delete import ApiTokenDelete


class IApiTokenRepository(ABC):
    @abstractmethod
    def save(
        self,
        config: Config,
        params: ApiToken,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def update(
        self,
        config: Config,
        params: ApiTokenUpdate,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def list(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def delete(
        self,
        config: Config,
        params: ApiTokenDelete,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def read(
        self,
        config: Config,
        params: ApiTokenRead,
    ) -> Union[Dict, None]:
        pass
        