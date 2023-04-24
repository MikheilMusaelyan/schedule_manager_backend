from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base.models import Post
from base.serializers import PostSerializer

    
class PostView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            post = Post.objects.get(pk=pk)
            if post is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            postSerializer = PostSerializer(post)
            return Response(postSerializer.data)
        else:
            posts = Post.objects.all()
            postSerializer = PostSerializer(posts, many=True)
            return Response(postSerializer.data)