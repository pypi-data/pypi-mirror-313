from typing import Dict, Union
from abc import ABC, abstractmethod
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.domain.models.apis.platform.entities.user.index import (
    UserDelete,
    UserRead,
    UserUpdate,
    UserSave,
)

class IUserRepository(ABC):
    @abstractmethod
    def save(
        self,
        config: Config,
        params: UserSave,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def update(
        self,
        config: Config,
        params: UserUpdate,
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
        params: UserDelete,
    ) -> Union[Dict, None]:
        pass

    @abstractmethod
    def read(
        self,
        config: Config,
        params: UserRead,
    ) -> Union[Dict, None]:
        pass
