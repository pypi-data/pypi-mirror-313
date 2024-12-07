from typing import Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.response import Response
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.apis.platform.entities.user.index import User, UserRead
from src.domain.services.repositories.apis.platform.entities.i_user_repository import (
    IUserRepository,
)
from src.core.classes.message import Message
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.models.message import MessageCoreEntity


class UserReadUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_A_P_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: UserRead,
    ) -> Union[User, str, None]:
        result: Response = await self.user_repository.read(config=config, params=params)
        if not result:
            return self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_RECORD_NOT_FOUND.value
                ),
            )

        user = User(**result.get("response"))
        return user
