from django import forms
from django.core.validators import RegexValidator


class CalculationForm(forms.Form):
    alphanumeric = RegexValidator(r'^[a-zA-Z]+$', 'Only alphabets are allowed.')

    description = forms.CharField(label='Description', max_length=100, widget=forms.TextInput(
        attrs={'pattern': '^[A-Za-z ]+$', 'title': 'Enter Characters Only '}))
    total_price = forms.IntegerField(label='Total Price', min_value=0, initial=0, disabled=True)
    group_id = forms.IntegerField(max_value=100, widget=forms.HiddenInput())
    number_of_ppl = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, n, *args, **kwargs):
        super(CalculationForm, self).__init__(*args, **kwargs)

        for i in range(n):
            self.fields['person_%s' % (i + 1)] = forms.IntegerField(label='share per person ', min_value=0,
                                                                    widget=forms.NumberInput(
                                                                        attrs={'onchange': 'adjust_price()'}))
