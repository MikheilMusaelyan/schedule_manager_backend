from django.urls import path
from rest_framework_simplejwt import views
from base.views import PostView, EventView, index

urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post/', PostView.as_view(), name='posts'),
    path('event/', EventView.as_view(), name='event'),
    path('c/', index.as_view(), name='index')
]