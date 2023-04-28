from django.urls import path
from rest_framework_simplejwt import views
from base.views import EventView, SingupView, LoginView

urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),

    path('event/signup/', SingupView.as_view(), name='signup'),
    
    path('event/', EventView.as_view(), name='event'),
    path('event/<int:bool>/', EventView.as_view(), name='event'),

    path('sami/', LoginView.as_view(), name='sami'),

    # path('index/', index.as_view(), name='index'),
]