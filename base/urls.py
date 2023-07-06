from django.urls import path
from rest_framework_simplejwt import views
from base.views import EventView, SingupView, LoginView, SearchEvents, index, getUpcomingEvents, sendMail

urlpatterns = [
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('signup/', SingupView.as_view(), name='signup'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('event/', EventView.as_view(), name='eventz'),
    path('event/<pk>/', EventView.as_view(), name='eventz'),
    path('event/<day>/<month>/<year>/', EventView.as_view(), name='eventz'),

    path('search/<date>/<start>/<name>/', SearchEvents.as_view(), name='s'),
    path('upcoming/', getUpcomingEvents.as_view(), name='upcoming'),

    path('index/', index.as_view(), name='index'),

    path('sendmail/', sendMail.as_view(), name='sendmail'),
]