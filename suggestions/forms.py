from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(
        attrs={'class':'form-control', 'pattern': '^[A-Za-z ]+$', 'title': 'Enter Characters Only '}))
    mobile_number = forms.CharField(label='Mobile Number', widget=forms.TextInput(
        attrs={'class':'form-control', 'pattern': '^[987][0-9]{9}$', 'title': 'Enter valid mobile number'}))
    feedback = forms.CharField(label='Tell us how we can improve:', widget=forms.Textarea(
        attrs={ 'class':'form-control', 'maxlength':'500', 'rows':'7'}
    ))
