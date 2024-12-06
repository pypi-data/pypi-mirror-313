import datetime
import json
from collections.abc import Iterable

from eveuniverse.models import EveEntity, EveMarketGroup, EveRegion, EveType

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from django.db.models.expressions import Case, When
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist

from allianceauth.services.hooks import get_extension_logger
from esi.decorators import token_required

from marketmanager.app_settings import (
    MARKETMANAGER_TYPESTATISTICS_MINIMUM_ORDER_COUNT,
)
from marketmanager.models import (
    Order, PublicConfig, Structure, SupplyConfig, TypeStatistics,
)

logger = get_extension_logger(__name__)

CHARACTER_SCOPES = [
    'esi-markets.read_character_orders.v1',
    'esi-markets.structure_markets.v1',
    'esi-universe.read_structures.v1',
]

CORPORATION_SCOPES = [
    'esi-markets.read_corporation_orders.v1',
    'esi-markets.structure_markets.v1',
    'esi-characters.read_corporation_roles.v1',
    'esi-corporations.read_structures.v1',
    'esi-universe.read_structures.v1',
]


@login_required
@permission_required("marketmanager.basic_market_browser")
def marketbrowser(request) -> HttpResponse:
    region_id = request.GET.get('region_id', None)
    type_id = request.GET.get('type_id', None)
    all_regions = PublicConfig.get_solo().fetch_regions.all()
    parent_market_groups = EveMarketGroup.objects.filter(
        parent_market_group_id__isnull=True)

    try:
        eve_type, eve_type_fetched = EveType.objects.get_or_create_esi(
            id=type_id)
    except Exception:
        eve_type = None

    try:
        eve_region, everegion_fetched = EveRegion.objects.get_or_create_esi(
            id=region_id)
    except Exception:
        eve_region = None

    if eve_type is not None:
        eve_type_icon_url = eve_type.icon_url(size=256)
    else:
        eve_type_icon_url = None

    render_items = {
        "all_regions": all_regions,
        "parent_market_groups": parent_market_groups,
        "eve_region": eve_region,
        "eve_type": eve_type,
        "eve_type_icon_url": eve_type_icon_url,
        "type_statistics": type_statistics(eve_type=eve_type, eve_region=eve_region),
    }
    try:
        # AA 4.x
        return render(request, "marketmanager/marketbrowser-bs5.html", render_items)
    except TemplateDoesNotExist:
        # AA 3.x
        return render(request, "marketmanager/marketbrowser.html", render_items)


@login_required
@permission_required("marketmanager.basic_market_watches")
def marketwatches(request) -> HttpResponse:

    watchconfigs = SupplyConfig.objects.all().annotate(
        missing_volume=F("volume") - F("last_result_volume")
    ).filter(
        missing_volume__gt=0)
    render_items = {
        "watchconfigs": watchconfigs,
    }
    try:
        # AA 4.x
        return render(request, "marketmanager/marketwatches-bs5.html", render_items)
    except TemplateDoesNotExist:
        # AA 3.x
        return render(request, "marketmanager/marketwatches.html", render_items)


@login_required
@permission_required("marketmanager.basic_market_browser")
def marketbrowser_autocomplete(request) -> HttpResponse:
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # is_ajax
        search_query = request.GET.get('term')

    autocomplete_query = EveType.objects.filter(
        name__icontains=search_query,
        eve_market_group__isnull=False,
        published=1
    ).order_by("name")

    result = []
    for possible in autocomplete_query:
        data = {}
        data['label'] = possible.name
        data['value'] = possible.id
        result.append(data)
    dump = json.dumps(result)

    mimetype = 'application/json'
    return HttpResponse(dump, mimetype)


@login_required
@permission_required("marketmanager.basic_market_browser")
def marketbrowser_buy_orders(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # is_ajax
        region_id = request.GET.get('region_id', None)
        type_id = request.GET.get('type_id', None)
    else:
        region_id = None
        type_id = None

    if request.user.has_perm("marketmanager.order_highlight_user"):
        user_characters = request.user.character_ownerships.all(
        ).select_related('character').values('character')
    else:
        user_characters = []

    if request.user.has_perm("marketmanager.order_highlight_corporation"):
        user_corporation_ids = request.user.character_ownerships.all().select_related(
            'character__corporation_id').values('character__corporation_id')
    else:
        user_corporation_ids = []

    buy_orders = Order.objects.filter(
        eve_type=type_id,
        is_buy_order=True
    ).annotate(
        user_is_owner=Case(
            When(
                issued_by_character__in=user_characters,
                then=True
            ),
            default=False
        ),
        corporation_is_owner=Case(
            When(
                issued_by_corporation__corporation_id__in=user_corporation_ids,
                then=True
            ),
            default=False
        ),
    ).values(
        'volume_remain',
        'price',
        'location_id',
        'issued',
        'duration',
        'eve_region__name',
        'updated_at',
        'user_is_owner',
        'corporation_is_owner'
    )
    if region_id is not None:
        buy_orders = buy_orders.filter(
            eve_region=region_id
        )

    buy_order_locations = []
    for order in buy_orders:
        buy_order_locations.append(order['location_id'])
    eveentities_resolved, structures_resolved = bulk_location_resolver(
        buy_order_locations)

    for order in buy_orders:
        if eveentities_resolved.to_name(order['location_id']) != "":
            order['location_resolved'] = eveentities_resolved.to_name(
                order['location_id'])
        else:
            try:
                order['location_resolved'] = structures_resolved[order['location_id']].name
            except KeyError:
                order['location_resolved'] = order['location_id']
        order["expiry_calculated"] = order["issued"] + \
            datetime.timedelta(days=order["duration"])

    return JsonResponse({"buy_orders": list(buy_orders)})


@login_required
@permission_required("marketmanager.basic_market_browser")
def marketbrowser_sell_orders(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # is_ajax
        region_id = request.GET.get('region_id', None)
        type_id = request.GET.get('type_id', None)
    else:
        region_id = None
        type_id = None

    if request.user.has_perm("marketmanager.order_highlight_user"):
        user_characters = request.user.character_ownerships.all(
        ).select_related('character').values('character')
    else:
        user_characters = []

    if request.user.has_perm("marketmanager.order_highlight_corporation"):
        user_corporation_ids = request.user.character_ownerships.all().select_related(
            'character__corporation_id').values('character__corporation_id')
    else:
        user_corporation_ids = []

    # Sell Orders
    sell_orders = Order.objects.filter(
        eve_type=type_id,
        is_buy_order=False
    ).annotate(
        user_is_owner=Case(
            When(
                issued_by_character__in=user_characters,
                then=True
            ),
            default=False
        ),
        corporation_is_owner=Case(
            When(
                issued_by_corporation__corporation_id__in=user_corporation_ids,
                then=True
            ),
            default=False
        ),
    ).values(
        'volume_remain',
        'price',
        'location_id',
        'issued',
        'duration',
        'eve_region__name',
        'updated_at',
        'order_id',
        'user_is_owner',
        'corporation_is_owner'
    )

    if region_id is not None:
        sell_orders = sell_orders.filter(
            eve_region=region_id
        )

    sell_order_locations = []
    for order in sell_orders:
        sell_order_locations.append(order['location_id'])
    eveentities_resolved, structures_resolved = bulk_location_resolver(
        sell_order_locations)

    for order in sell_orders:
        if eveentities_resolved.to_name(order['location_id']) != "":
            order['location_resolved'] = eveentities_resolved.to_name(
                order['location_id'])
        else:
            try:
                order['location_resolved'] = structures_resolved[order['location_id']].name
            except KeyError:
                order['location_resolved'] = order['location_id']
        order["expiry_calculated"] = order["issued"] + \
            datetime.timedelta(days=order["duration"])

    return JsonResponse({"sell_orders": list(sell_orders)})


@login_required
@permission_required("marketmanager.basic_market_browser")
def item_selector(request):
    data = EveMarketGroup.objects.all()
    return render(request, "marketmanager/item_selector.html", data)


@login_required
@token_required(scopes=CHARACTER_SCOPES)
def add_char(request, token):
    return redirect('marketmanager:marketbrowser')


@login_required
@token_required(scopes=CORPORATION_SCOPES)
def add_corp(request, token):
    return redirect('marketmanager:marketbrowser')


def location_resolver(location_id) -> str:
    if location_id >= 60000000 and location_id <= 64000000:
        # EveStation (Range: 60000000 - 64000000)
        # EveEntity has its own resolver
        # but i dont want Structures to slip through
        # and spam ESI errors
        return EveEntity.objects.resolve_name(location_id)
    else:
        try:
            return Structure.objects.get(structure_id=location_id).name
        except Exception as e:
            logger.exception(e)
            return str(location_id)


def bulk_location_resolver(location_ids: Iterable[int]):
    bulk_eve_entity_ids = []
    bulk_structure_ids = []

    for location_id in location_ids:
        if location_id >= 60000000 and location_id <= 64000000:
            # EveStation (Range: 60000000 - 64000000)
            # EveEntity has its own resolver
            # but i dont want Structures to slip through
            # and spam ESI errors
            bulk_eve_entity_ids.append(location_id)
        else:
            bulk_structure_ids.append(location_id)

    eveentity_resolver = EveEntity.objects.bulk_resolve_names(
        bulk_eve_entity_ids)
    structure_resolver = Structure.objects.in_bulk(bulk_structure_ids)

    return eveentity_resolver, structure_resolver


def type_statistics(eve_type: EveType, eve_region: EveRegion):
    # Returns a specific set of stats for the item_details template
    orders = Order.objects.filter(eve_type=eve_type)
    if eve_region is not None:
        orders = orders.filter(
            eve_region=eve_region
        )
    try:
        order_stats = TypeStatistics.objects.get(
            eve_type=eve_type, eve_region=eve_region)
    except ObjectDoesNotExist:
        return {
            'buy_fifth_percentile': 0,
            'sell_fifth_percentile': 0,
            'buy_weighted_average': 0,
            'sell_weighted_average': 0,
            'buy_median': 0,
            'sell_median': 0,
            'buy_volume': orders.filter(is_buy_order=True).aggregate(volume=Sum(F('volume_remain')))["volume"],
            'sell_volume': orders.filter(is_buy_order=False).aggregate(volume=Sum(F('volume_remain')))["volume"],
            'explain': f"TypeStatistics have not been calculated yet, or skipped due to less than {MARKETMANAGER_TYPESTATISTICS_MINIMUM_ORDER_COUNT} orders"
        }
    return {
        'buy_fifth_percentile': order_stats.buy_fifth_percentile,
        'sell_fifth_percentile': order_stats.sell_fifth_percentile,
        'buy_weighted_average': order_stats.buy_weighted_average,
        'sell_weighted_average': order_stats.sell_weighted_average,
        'buy_median': order_stats.buy_median,
        'sell_median': order_stats.sell_median,
        'buy_volume': orders.filter(is_buy_order=True).aggregate(volume=Sum(F('volume_remain')))["volume"],
        'sell_volume': orders.filter(is_buy_order=False).aggregate(volume=Sum(F('volume_remain')))["volume"],
        'explain': None
    }
