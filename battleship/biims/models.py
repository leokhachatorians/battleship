from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    
    storage_location = models.CharField(max_length=200)
    
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)

    last_reorder_date = models.DateTimeField('last reorder date', blank=True, null=True)
    last_reorder_quantity = models.IntegerField(default=0)

    is_easy_consumable = False
    is_low_volume = False
    is_asset = False

    def reorder_check(self):
        if self.quantity < self.reorder_point:
            return 'Need to reorder'

    def reduce_quantity(self, amount=1):
        self.quantity -= amount
        self.save()

    def increase_quantity(self, amount=1):
        self.quantity += amount
        self.save()

    class Meta:
        abstract = True

class HighVolume(Item):
    is_easy_consumable = True
    consumable_location = models.CharField(max_length=200)

class LowVolume(Item):
    is_low_volume = True

class Asset(Item):
    is_asset = True
