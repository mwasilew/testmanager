# Copyright (C) 2014 Linaro Limited
#
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>
#
# This file is part of Testmanager.
#
# Testmanager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation
#
# Testmanager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Testmanager.  If not, see <http://www.gnu.org/licenses/>.

from django.http import (
    HttpResponse, 
    HttpResponseServerError,
    HttpResponseRedirect,
)
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.template import RequestContext, loader
from testplanner.models import (
    TestPlan,
    TestPlanTestDefinition
)
from testplanner.forms import (
    TestPlanForm,
)

@login_required
def index(request):
    testplans = TestPlan.objects.all()
    template = loader.get_template('testplanner/index.html')
    context = RequestContext(request, {
        'testplans': testplans,
    })
    return HttpResponse(template.render(context))

@login_required
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
