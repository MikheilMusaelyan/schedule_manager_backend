from rest_framework import serializers
from base.models import Post, Event

class PostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Post
        fields = '__all__'