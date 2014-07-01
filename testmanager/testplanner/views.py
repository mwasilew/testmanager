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
import json 

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.template import RequestContext, loader
from django.core import serializers
from django.views.generic import TemplateView, View

from testmanager.testplanner.models import TestPlan, TestPlanTestDefinition
from testmanager.testplanner.forms import TestPlanForm


@login_required
def index(request):
    testplans = TestPlan.objects.all()
    template = loader.get_template('testplanner/index.html')
    context = RequestContext(request, {
        'testplans': testplans,
    })
    return HttpResponse(template.render(context))


class JSONView(View):

    def get_context_data(self):
        raise NotImplementedError("get_context_data not implemented")

    def get(self, request, *args, **kwargs):
        return HttpResponse(
            json.dumps(self.get_context_data()),
            content_type='application/json',
            **kwargs
        )


class NewView(TemplateView):
    template_name='testplanner/new.html'

    def get(self, request, *args, **kwargs):
        form = TestPlanForm()

        return super(NewView, self).get(request, **{
            "form": form
        })

    def post(self, request, *args, **kwargs):
        form = TestPlanForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/success/')

        return super(NewView, self).get(request, **{
            "form": form
        })


# class TestDefinitionsView(View):

#      def render_to_json_response(self, context, **response_kwargs):
#          return HttpResponse(
#              self.convert_context_to_json(context),
#              content_type='application/json',
#              **response_kwargs
#          )

#     def render_to_response(self, context, **response_kwargs):
#         return self.render_to_json_response(context, **response_kwargs)

#     def render_to_response(self, context, **response_kwargs):
#         import pdb; pdb.set_trace()
#         return self.render_to_json_response(context, **response_kwargs)


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
        'form': testplan_form,
        'testplan_formset': testplan_formset,
    })
    return HttpResponse(template.render(context))
