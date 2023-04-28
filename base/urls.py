from django.urls import path
from rest_framework_simplejwt import views
from base.views import EventView, SingupView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('signup/', SingupView.as_view(), name='signup'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('event/', EventView.as_view(), name='event'),
    path('event/<int:bool>/', EventView.as_view(), name='event'),

    # path('index/', index.as_view(), name='index'),
]