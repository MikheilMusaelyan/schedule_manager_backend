from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.models import Event
from base.serializers import EventSerializer

from .tasks import send_the_email
from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk=None):
        if pk is not None:
            event = Event.objects.get(pk=pk)
            eventSerializer = EventSerializer(event)
            if event is None:
                return Response(eventSerializer.errors, status=status.HTTP_404_NOT_FOUND)
            return Response(eventSerializer.data)
        
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        userID = request.GET.get('userId')

        events = Event.objects.filter(date__year=year, date__month=month, userId=userID)
        eventSerializer = EventSerializer(events, many=True)

        for date in eventSerializer.data:
            if str(date['date']) == f"{year}-{month}-{day}":
                date['requested_day'] = True
            else:
                date['requested_day'] = False
        
        return Response(eventSerializer.data)
    
    def post(self, request):
        eventSerializer = EventSerializer(data=request.data)

        if eventSerializer.is_valid():
            event = eventSerializer.validated_data
            
            if event.get('start') >= event.get('end'):
                event['end'] = event.get('start') + 1
                

            eventSerializer.save()
            return Response(eventSerializer.data, status=status.HTTP_201_CREATED)
        
        return Response(eventSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        eventSerializer = EventSerializer(event, data=request.data)

        if eventSerializer.is_valid():
            eventSerializer.save()
            return Response(eventSerializer.data, status=status.HTTP_200_OK)
        return Response(eventSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        Event.objects.filter(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class index(APIView):
    def get(self, request):
        send_the_email.delay(30, 'ss', ' dsa', 'sumemail')
        return Response({'msg': 'email sent'})