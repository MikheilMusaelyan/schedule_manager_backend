from django.urls import path
from rest_framework_simplejwt import views
from base.views import EventView, SingupView

urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),

    path('event/signup/', SingupView.as_view(), name='signup'),
    
    path('event/', EventView.as_view(), name='event'),
    path('event/<int:pk>/', EventView.as_view(), name='event'),

    # path('index/', index.as_view(), name='index'),
]