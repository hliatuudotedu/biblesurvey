from django import forms


class SurveyForm(forms.Form):
    patient_name = forms.CharField(
        required=True,
        max_length=255,
        min_length=1)
