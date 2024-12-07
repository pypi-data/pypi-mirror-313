from typing import List, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.classes.async_message import Message
from src.core.models.filter import Pagination
from src.core.models.response import Response
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.apis.platform.entities.user.index import User
from src.infrastructure.apis.platform.repositories.entities.user_repository import (
    UserRepository,
)


class UserListUseCase:
    def __init__(self):
        self.user_repository = UserRepository()
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_A_P_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[User], str, None]:
        result: Response = await self.user_repository.list(config=config, params=params)
        if not result:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_NO_RESULTS_FOUND.value
                ),
            )

        data = [User(**entity) for entity in result.get("response")]
        return data
