from rest_framework import serializers
from base.models import Event, CustomUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['start', 'end', 'date', 'color']

class SearchEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'is_staff']

# class CollabSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CollabMember
#         fields = '__all__'