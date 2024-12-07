
from typing import List, Union
from src.core.config import settings
from src.core.enums.layer import LAYER
from src.core.models.config import Config
from src.core.models.filter import Pagination
from src.core.classes.async_message import Message
from src.core.models.message import MessageCoreEntity
from src.core.enums.keys_message import KEYS_MESSAGES
from src.core.wrappers.execute_transaction import execute_transaction
from src.domain.models.apis.platform.entities.api_token.api_token import ApiToken
from src.infrastructure.apis.platform.repositories.entities.api_token_repository import ApiTokenRepository



class ApiTokenListUseCase:
    def __init__(self):
        self.api_token_repository = ApiTokenRepository()
        self.message = Message()

    @execute_transaction(layer=LAYER.D_S_U_E.value, enabled=settings.has_track)
    async def execute(
        self,
        config: Config,
        params: Pagination,
    ) -> Union[List[ApiToken], str, None]:
        results = await self.api_token_repository.list(config=config, params=params)
        if not results:
            return await self.message.get_message(
                config=config,
                message=MessageCoreEntity(
                    key=KEYS_MESSAGES.CORE_NO_RESULTS_FOUND.value
                ),
            )
        
        data = [ApiToken(**entity) for entity in results.get("response")]
        return data
        