from rest_framework import serializers
from base.models import Post, Event

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'