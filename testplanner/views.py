from django.http import (
    HttpResponse, 
    HttpResponseServerError,
    HttpResponseRedirect,
)
from django.forms.models import inlineformset_factory
from django.template import RequestContext, loader
from testplanner.models import (
    TestPlan,
    TestPlanTestDefinition
)
from testplanner.forms import (
    TestPlanForm,
)


def index(request):
    testplans = TestPlan.objects.all()
    template = loader.get_template('testplanner/index.html')
    context = RequestContext(request, {
        'testplans': testplans,
    })
    return HttpResponse(template.render(context))

def testplan_new(request):
    testplan = TestPlan()
    TestplanFormset = inlineformset_factory(
        TestPlan, 
        TestPlanTestDefinition,
        extra=1,
        can_delete=False)
    if request.POST:
        testplan_formset = TestplanFormset(request.POST, instance=testplan)
        testplan_form = TestPlanForm(request.POST, instance=testplan)
        if testplan_form.is_valid() and testplan_formset.is_valid():
            testplan_form.save()
            testplan_formset.save()
            return HttpResponseRedirect('/testplanner')
    else:
        testplan_form = TestPlanForm(instance=testplan)
        testplan_formset = TestplanFormset(instance=testplan)
    template = loader.get_template('testplanner/new.html')
    context = RequestContext(request, {
        'testplan_form': testplan_form,
        'testplan_formset': testplan_formset,
    })
    return HttpResponse(template.render(context))
