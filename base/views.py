from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.models import Event, CustomUser, Mail
from base.serializers import EventSerializer

from datetime import datetime

from django.db.models import Q
    
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        userID = request.user.id

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
            event['userId'] = request.user
            
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
    
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = datetime.now()
        year = now.year
        month = str(now.month).zfill(2)
        day = now.day

        upcomingEvents = Event.objects.filter(userId=user.id).order_by('date', 'start')[:3]
        
        events = Event.objects.filter(date__year=year, date__month=month, userId=user.id)
        eventSerializer = EventSerializer(events, many=True)

        for date in eventSerializer.data:
            if str(date['date']) == f"{year}-{month}-{day}":
                date['requested_day'] = True
            else:
                date['requested_day'] = False

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'events': eventSerializer.data
        }, status=status.HTTP_200_OK)

class SingupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.create_user(email=email, password=password, **kwargs,)
        except ValueError as error:
            return Response(str(error), status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class SearchEvents(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.GET.get('name')
        start = request.GET.get('start')
        day = request.GET.get('day')
        month = request.GET.get('month')
        year = request.GET.get('year')

        user_id = int(request.user.id)


        filter_condition = Q(userId=user_id)

        if name:
            filter_condition &= Q(name__icontains=name)
        if start:
            filter_condition &= Q(start=start)
        if year:
            filter_condition &= Q(date__year=year)
        if month:
            filter_condition &= Q(date__month=month)
        if day:
            filter_condition &= Q(date__day=day)

        events = Event.objects.filter(filter_condition)
        eventSerializer = EventSerializer(events, many=True)

        return Response(eventSerializer.data)
    
# from base.tasks import send_the_email
# class index(APIView):
    # permission_classes = [AllowAny]
    # def get(req,self):
    #     send_the_email.delay()
    #     return Response({'msg': 'hi'})
    
# class Colaborations(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         eventId = request.POST.get('eventId')
#         otherUserId = request.POST.get('otherUserId')
        
#         event = Event.objects.filter(id=eventId)
#         if event.userId != request.user.id:
#             return

#         colabSerializer = CollabSerializer(request.data)
#         if colabSerializer.is_valid:
#             colabSerializer.save()
#             return Response(colabSerializer.data, status=status.HTTP_201_CREATED)
#         return Response(colabSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

