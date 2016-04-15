from django import forms

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
                ('Item Type', 'Asset'),
                ('Item Type', 'Low Volume'),
                ('Item Type', 'High Volume')])

    item_name = forms.CharField(
            max_length=100,
            label='Item Name',
            widget=forms.TextInput(attrs=
                {'placeholder':'Name',
                'title':'Name of the item',
                'id':'item-name'}))

    quantity = forms.CharField(
        max_length=10,
        label='Quantity',
        widget = forms.NumberInput(attrs=
            {'placeholder':'Quantity',
            'title':'How many?',
            'id':'item-quantity'}))

    storage_location = forms.CharField(
        max_length=100,
        label='Storage Location',
        widget = forms.TextInput(attrs=
            {'placeholder':'Storage Location',
            'title':'Where the items reserves will be kept',
            'id':'item-storage-location'}))

    consumable_location = forms.CharField(
        max_length=100,
        label='Consumable Location',
        widget = forms.TextInput(attrs=
            {'placeholder':'Consumable Location',
            'title':'Location where staff members can get the item',
            'id':'item-storage-location'}))

    reorder_point = forms.CharField(
        max_length=10,
        label='Reorder Point',
        widget = forms.TextInput(attrs=
            {'placeholder':'Reorder Point',
            'title':'When to reorder the item',
            'id':'item-reorder-point'}))
