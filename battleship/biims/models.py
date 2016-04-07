from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200)
    
    storage_location = models.CharField(max_length=200)

    is_consumable = models.BooleanField(default=False)
    consumable_location = models.CharField(max_length=200)

    is_asset = models.BooleanField(default=False)
    asset_location = models.CharField(max_length=200)
    
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)

    last_reorder_date = models.DateTimeField('last reorder date')
    last_reorder_quantity = models.IntegerField(default=0)
