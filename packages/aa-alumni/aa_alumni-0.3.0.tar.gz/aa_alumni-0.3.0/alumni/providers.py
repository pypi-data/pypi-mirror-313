from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi import __version__ as esi__version__
from esi.clients import EsiClientProvider

from . import __version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"aa-alumni/{__version__} allianceauth/{aa__version__} django-esi/{esi__version__}"

"""
Swagger spec operations:
get_corporations_corporation_id_alliancehistory
get_characters_character_id_corporationhistory
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_corporations_corporation_id_alliancehistory(corporation_id: int) -> dict:
    result = esi.client.Corporation.get_corporations_corporation_id_alliancehistory(
        corporation_id=corporation_id
    ).results()
    return result


def get_characters_character_id_corporationhistory(character_id: int) -> dict:
    result = esi.client.Character.get_characters_character_id_corporationhistory(
        character_id=character_id
    ).results()
    return result
