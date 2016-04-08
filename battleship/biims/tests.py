import datetime

from django.utils import timezone
from django.test import TestCase

from biims.models import HighVolume, LowVolume, Asset

class ItemTestCase(TestCase):
    def test_high_volume_is_easy_consumbale(self):
        item = HighVolume()
        self.assertTrue(item.is_easy_consumable)

    def test_high_volume_is_not_low_volume(self):
        item = HighVolume()
        self.assertFalse(item.is_low_volume)

    def test_high_volume_is_not_asset(self):
        item = HighVolume()
        self.assertFalse(item.is_asset)

    def test_low_volume_is_not_easy_consumable(self):
        item = LowVolume()
        self.assertFalse(item.is_easy_consumable)

    def test_low_volume_is_low_volume(self):
        item = LowVolume()
        self.assertTrue(item.is_low_volume)

    def test_low_volume_is_not_asset(self):
        item = LowVolume()
        self.assertFalse(item.is_asset)

    def test_asset_is_not_easy_consumable(self):
        item = Asset()
        self.assertFalse(item.is_easy_consumable)

    def test_asset_is_not_low_volume(self):
        item = Asset()
        self.assertFalse(item.is_low_volume)

    def test_asset_is_asset(self):
        item = Asset()
        self.assertTrue(item.is_asset)

    def test_reorder_works(self):
        item = Asset(
                quantity=1,
                reorder_point=5)

        self.assertEqual(item.reorder_check(), "Need to reorder")
