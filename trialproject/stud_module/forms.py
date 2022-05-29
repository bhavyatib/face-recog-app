from django import forms

# Form to handle edge cases. 
class DateForm(forms.Form):
	date = forms.CharField(required=True)
