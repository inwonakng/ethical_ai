from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import * 

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class SurveySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Survey
        fields = ['desc','prompt','user']

class ScenarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scenario
        fields = []
    def to_representation(self,instance):
        # ret = super().to_representation(instance)
        return instance.object_form()


