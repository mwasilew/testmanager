from django import forms
from testrunner.models import LavaJobResult 


class ResultComparisonForm(forms.Form):
    testresults = forms.ModelMultipleChoiceField(
        queryset = LavaJobResult.objects.all(),
        widget  = forms.CheckboxSelectMultiple
    )
