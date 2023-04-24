from django.urls import path
from base.views import PostView

urlpatterns = [
    path('post/', PostView.as_view(), name='posts'),
]