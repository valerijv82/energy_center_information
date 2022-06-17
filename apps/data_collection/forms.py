from django import forms


class MyForm(forms.Form):
    customer = forms.ChoiceField(label='Customers')
    from_year_mo = forms.ChoiceField(label='Date From')
    to_year_mo = forms.ChoiceField(label='To')
