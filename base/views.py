from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from base.models import Event
from base.serializers import EventSerializer

from .tasks import send_the_email
from django_celery_beat.models import PeriodicTask, IntervalSchedule
    
class EventView(APIView):
    
    def get(self, request, pk=None):
        if pk is not None:
            event = Event.objects.get(pk=pk)
            eventSerializer = EventSerializer(event)
            if event is None:
                return Response(eventSerializer.errors, status=status.HTTP_404_NOT_FOUND)
            return Response(eventSerializer.data)
        
        events = Event.objects.all()
        eventSerializer = EventSerializer(events, many=True)
        return Response(eventSerializer.data)
    
    def post(self, request):
        eventSerializer = EventSerializer(data=request.data)

        if eventSerializer.is_valid():
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
    
