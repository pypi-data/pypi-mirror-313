from eveuniverse.models import EveType

from django.test import TestCase

from allianceauth.authentication.models import EveCharacter

from marketmanager.models import Order

from .testdata.load_eveuniverse import load_eveuniverse


def create_testdata():
    load_eveuniverse()
    EveCharacter.objects.all().delete()
    EveCharacter.objects.create(
        character_id=1,
        character_name='Character1',
        corporation_id=1,
        corporation_name='test corp',
        corporation_ticker='TEST'
    )
    EveCharacter.objects.create(
        character_id=2,
        character_name='Character2',
        corporation_id=1,
        corporation_name='test corp',
        corporation_ticker='TEST'
    )
    Order.objects.create(
        # expired order
        eve_type=EveType.objects.get(id=44992)
    )


class TestMarketmanagerTasks(TestCase):
    def test_garbage_collection(self):
        # Orders
        # Generic Expiry Date Passed

        # Calculated Expiry Date Passed

        # State = Expired or Cancelled

        # Stale

        # Structures
        # Stale
        self.assertTrue(True)
