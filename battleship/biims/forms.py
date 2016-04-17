from django import forms

from django.core.exceptions import ValidationError
from django.template.defaultfilters import mark_safe

class SearchForm(forms.Form):
    search_text = forms.CharField(
            max_length=100,
            label='',
            widget=forms.TextInput(attrs=
                {'placeholder': 'Search',
                'class':'search-query form-control',
                'id':'search-term',}))
 
class NewItemForm(forms.Form):
    item_type = forms.ChoiceField(choices=
            [
                ('asset', 'Asset'),
                ('low', 'Low Volume'),
                ('high', 'High Volume')],
            required=True,
            widget = forms.Select(attrs={
                'id':'item-choice-selector'}))

    item_name = forms.CharField(
            max_length=100,
            label='Item Name',
            widget=forms.TextInput(attrs=
                {'placeholder':'Name',
                'title':'Name of the item',
                'id':'item-name'}),
            required=True)

    quantity = forms.CharField(
        max_length=10,
        label='Quantity',
        widget = forms.NumberInput(attrs=
            {'placeholder':'Quantity',
            'title':'How many?',
            'id':'item-quantity'}),
        required=True)

    storage_location = forms.CharField(
        max_length=100,
        label='Storage Location',
        widget = forms.TextInput(attrs=
            {'placeholder':'Storage Location',
            'title':'Where the items reserves will be kept',
            'id':'item-storage-location'}),
        required=True)

    consumable_location = forms.CharField(
        max_length=100,
        label='Consumable Location',
        widget = forms.TextInput(attrs=
            {'placeholder':'Consumable Location',
            'title':'Location where staff members can get the item',
            'id':'item-consumable-location'}),
        required=False)

    reorder_point = forms.CharField(
        max_length=10,
        label='Reorder Point',
        widget = forms.TextInput(attrs=
            {'placeholder':'Reorder Point',
            'title':'When to reorder the item',
            'id':'item-reorder-point'}),
        required=True)

    def __init__(self, data=None, *args, **kwargs):
        super(NewItemForm, self).__init__(data, *args, **kwargs)

        if data and data.get('item_type', None) == 'high':
            self.fields['consumable_location'].required = True

        
