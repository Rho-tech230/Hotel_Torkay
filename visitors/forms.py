from django import forms
from datetime import datetime

class AvailabilityCheckForm(forms.Form):
    entry_date = forms.DateField(initial=datetime.today())
    exit_date = forms.DateField(initial=datetime.today())




