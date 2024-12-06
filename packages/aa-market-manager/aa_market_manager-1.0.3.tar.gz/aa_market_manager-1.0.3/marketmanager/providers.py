from allianceauth import __version__ as aa__version__
from allianceauth.services.hooks import get_extension_logger
from esi import __version__ as esi__version__
from esi.clients import EsiClientProvider
from esi.models import Token

from . import __version__

logger = get_extension_logger(__name__)

APP_INFO_TEXT = f"aa-market-manager/{__version__} (https://gitlab.com/tactical-supremacy/aa-market-manager) allianceauth/{aa__version__} django-esi/{esi__version__}"
"""
Swagger spec operations:
get_universe_structures
get_universe_structures_structure_id
get_markets_region_id_orders
get_markets_structures_structure_id
get_characters_character_id_orders
get_characters_character_id_orders_history
get_corporations_corporation_id_orders
get_corporations_corporation_id_orders_history
get_corporations_corporation_id_structures
"""

esi = EsiClientProvider(app_info_text=APP_INFO_TEXT)


def get_universe_structures(filter: str = "all"):
    result = esi.client.Universe.get_universe_structures(
        filter=filter
    ).results()
    return result


def get_universe_structures_structure_id(structure_id: int, token: Token):
    return esi.client.Universe.get_universe_structures_structure_id(structure_id=structure_id, token=token.valid_access_token()).results()


def get_markets_region_id_orders(
        region_id: int,
        order_type: str = "all"):
    result = esi.client.Market.get_markets_region_id_orders(
        order_type=order_type,
        region_id=region_id
    ).results()
    return result


def get_markets_region_id_orders_paged(
        region_id: int,
        page: int,
        order_type: str = "all"):
    result = esi.client.Market.get_markets_region_id_orders(
        order_type=order_type,
        region_id=region_id,
        page=page
    )
    result.request_config.also_return_response = True
    return result.result()


def get_markets_region_id_orders_by_typeid(
        region_id: int,
        order_type: str = "all",
        type_id: str = ""):
    result = esi.client.Market.get_markets_region_id_orders(
        order_type=order_type,
        region_id=region_id,
        type_id=type_id
    ).results()
    return result


def get_markets_region_id_orders_by_typeid_paged(
        region_id: int,
        page: int,
        order_type: str = "all",
        type_id: str = ""):
    result = esi.client.Market.get_markets_region_id_orders(
        order_type=order_type,
        region_id=region_id,
        type_id=type_id,
        page=page
    )
    result.request_config.also_return_response = True
    return result.result()


def get_markets_region_id_history(
        region_id: int,
        order_type: str = "all",
        type_id: str = ""):
    result = esi.client.Market.get_markets_region_id_history(
        order_type=order_type,
        region_id=region_id,
        type_id=type_id
    ).results()
    return result


def get_markets_structures_structure_id(structure_id: int, token: Token):
    result = esi.client.Market.get_markets_structures_structure_id(
        structure_id=structure_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_characters_character_id_orders(character_id: int):
    required_scopes = ['esi-markets.read_character_orders.v1']
    token = Token.get_token(character_id, required_scopes)

    result = esi.client.Market.get_characters_character_id_orders(
        character_id=character_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_characters_character_id_orders_history(character_id: int):
    required_scopes = ['esi-markets.read_character_orders.v1']
    token = Token.get_token(character_id, required_scopes)

    result = esi.client.Market.get_characters_character_id_orders_history(
        character_id=character_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_characters_character_id_roles_from_token(token: Token):
    # Yes this is weird, its because im pulling _specific_ scopes to find this token elsewhere
    result = esi.client.Character.get_characters_character_id_roles(
        character_id=token.character_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_corporations_corporation_id_orders(corporation_id: int, token: Token):
    result = esi.client.Market.get_corporations_corporation_id_orders(
        corporation_id=corporation_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_corporations_corporation_id_orders_history(corporation_id: int, token: Token):
    result = esi.client.Market.get_corporations_corporation_id_orders_history(
        character_id=corporation_id,
        token=token.valid_access_token()
    ).results()
    return result


def get_corporations_corporation_id_structures(corporation_id: int, token: Token):
    result = esi.client.Corporation.get_corporations_corporation_id_structures(
        corporation_id=corporation_id,
        token=token.valid_access_token()
    ).results()
    return result
