from __future__ import unicode_literals
from django.views.generic import TemplateView

from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView

from testmanager.testmanualrunner import models
from testmanager.testrunner import models as testrunner_models
from testmanager.testplanner import views as testplanner_views, models as testplanner_models

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.compat import smart_text


class Base(TemplateView):
    template_name='testmanualrunner/base.html'


#### serializers ####

class RelatedObject(serializers.RelatedField):

    def __init__(self, *args, **kwargs):
        self.serializer = kwargs.pop("serializer", None)
        assert self.serializer, 'serializer is required'
        super(RelatedObject, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        return "%s - %s" % (smart_text(obj), obj.pk)

    def prepare_value(self, obj):
        return obj.pk

    def to_native(self, pk):
        return self.serializer(pk).data

    def from_native(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a `queryset` argument')

        try:
            return self.queryset.get(pk=data)
        except ObjectDoesNotExist:
            msg = self.error_messages['does_not_exist'] % smart_text(data)
            raise ValidationError(msg)
        except (TypeError, ValueError):
            received = type(data).__name__
            msg = self.error_messages['incorrect_type'] % received
            raise ValidationError(msg)



class TestRunResult(serializers.ModelSerializer):
    class Meta:
        model = models.TestRunResult


class TestRun(serializers.ModelSerializer):
    test_plan = RelatedObject(read_only=True, serializer=testplanner_views.TestPlanSerializer)
    tests_definitions_results = TestRunResult(many=True, read_only=True)
    build = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.TestRun


class JenkinsBuild(serializers.ModelSerializer):
    class Meta:
        model = testrunner_models.JenkinsBuild



class TestStatus(serializers.ModelSerializer):
    class Meta:
        model = models.TestStatus

#### views ####


class TestRun_ListCreate_View(generics.ListCreateAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun


class TestRun_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRun.objects.all()
    serializer_class = TestRun


class Build_List_View(generics.ListAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class Build_Details_View(generics.RetrieveAPIView):
    queryset = testrunner_models.JenkinsBuild.objects.all()
    serializer_class = JenkinsBuild


class TestStatus_List_View(generics.ListAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestStatus_Details_View(generics.RetrieveAPIView):
    queryset = models.TestStatus.objects.all()
    serializer_class = TestStatus


class TestRunResult_Details_View(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResult


class TestRunResult_ListCreate_View(generics.ListCreateAPIView):
    queryset = models.TestRunResult.objects.all()
    serializer_class = TestRunResult


# class DefinitionYamlFile(APIView):
    # def get(self, request, test_definition_id, format=None):
    #     test_plan_test_definition = testplanner_models.TestPlanTestDefinition(pk=test_definition_id)
    #     import pdb; pdb.set_trace()
    # snippets = Snippet.objects.all()
    # serializer = SnippetSerializer(snippets, many=True)
    # return Response(serializer.data)
