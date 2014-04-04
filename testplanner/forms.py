from django.forms import ModelForm
from testplanner.models import (
    TestPlan,
)


class TestPlanForm(ModelForm):
    class Meta:
        model = TestPlan
