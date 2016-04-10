from django import forms

class SearchForm(forms.Form):
    search_text = forms.CharField(
            max_length=100,
            label='',
            widget=forms.TextInput(attrs=
                {'placeholder': 'Search',
                'class':'search-query form-control',
                'id':'search-term'}))
