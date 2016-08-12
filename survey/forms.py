from django import forms


class SurveyForm(forms.Form):
    patient_name = forms.CharField(
        required=True,
        max_length=255,
        min_length=1)


class ImportQuestionsChoicesForm(forms.Form):
    all_info = forms.CharField(
        required=True, widget=forms.Textarea(
            attrs={'rows': 10, 'cols': 80}))


