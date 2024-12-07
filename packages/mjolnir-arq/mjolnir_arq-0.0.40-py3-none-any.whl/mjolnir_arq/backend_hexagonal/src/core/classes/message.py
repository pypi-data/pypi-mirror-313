from src.core.models.config import Config
from src.core.models.message import MessageCoreEntity
from src.infrastructure.database.entities.language_entity import LanguageEntity
from src.infrastructure.database.entities.translation_entity import TranslationEntity
from src.infrastructure.database.mappers.translation_mapper import map_to_translation


class Message:

    def get_message(cls, config: Config, message: MessageCoreEntity):
        db = config.db
        result = (
            db.query(TranslationEntity, LanguageEntity)
            .join(
                LanguageEntity, TranslationEntity.language_code == LanguageEntity.code
            )
            .filter(
                TranslationEntity.context == message.context,
                TranslationEntity.key == message.key,
                LanguageEntity.code == config.language,
            )
            .first()
        )
        if not result:
            return "Message not configurated"
        translation, language = result
        text = map_to_translation(translation)
        return f"{text.translation}"
