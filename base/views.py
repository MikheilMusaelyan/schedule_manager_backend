from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.models import Event, CustomUser
from base.serializers import EventSerializer, CustomUserSerializer
    
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


class SingupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        print(email, username, password, '{"email": "myemail@gmail.com", "username": "nousernaem", "password": "Balishi1"}')
        try:
            user = CustomUser.objects.create_user(email=email, password=password, username=username, **kwargs)
        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
from base.tasks import send_the_email
class index(APIView):
    permission_classes = [AllowAny]
    def get(req,self):
        send_the_email.delay()
        return Response({'msg': 'hi'})
    
class Collaborations(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        otherUser = request.POST.get('user')
     