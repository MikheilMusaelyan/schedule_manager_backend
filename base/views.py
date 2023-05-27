from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.models import Event, CustomUser, Mail, Color
from base.serializers import EventSerializer, UpcomingEventSerializer, PutEventSerializer

from datetime import datetime
from django.db.models import Q
from datetime import datetime
    
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, day=None, month=None, year=None):
        userID = request.user.id

        events = Event.objects.select_related('color').filter(date__year=year, date__month=month, userId=userID)
        eventSerializer = EventSerializer(events, many=True)

        dateObject = {}
        now = datetime.now()

        year = now.year
        month = str(now.month).zfill(2)
        hour = now.hour * 4
        minute = now.minute

        hour += math.floor(minute / 15)
        print(userID)

        first_condition_events = Event.objects.select_related('color').filter(
            (Q(date=now.date()) & Q(start__gt=hour)),
            userId=userID
        ).order_by('start')[:3]
        
        remaining_events = Event.objects.select_related('color').filter(
            Q(date__gt=now.date()),
            userId=userID
        ).order_by('date', 'start')[:3 - first_condition_events.count()]
        
        upcomingEvents = list(first_condition_events) + list(remaining_events)
        upcomingEventSerializer = UpcomingEventSerializer(upcomingEvents, many=True)

        for event in eventSerializer.data:
            
            dayObject = datetime.strptime(event['date'], '%Y-%m-%d')
            dayObject = dayObject.replace(hour=7)
            formatted_date = dayObject.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            day = dayObject.day

            if f'd{day}' not in dateObject:
                dateObject[f'd{day}'] = []

            event['color'] = {
                'name' : event['color'],
                'pastel': False
            }
            event['date'] = formatted_date
            
            dateObject[f'd{day}'].append(event)

        return Response({
            'info': dateObject,
            'upcoming': upcomingEventSerializer.data
        })
    
    def post(self, request, pk=None):
        
        color = Color.objects.get_or_create(
            name = request.data.get('color').get('name'),
        )
        
        request.data['color'] = getattr(color[0], 'pk')
        eventSerializer = EventSerializer(data=request.data)
        
        if eventSerializer.is_valid():
            event = eventSerializer.validated_data
            event['userId'] = request.user
            
            if event.get('start') >= event.get('end'):
                event['end'] = event.get('start') + 1
        
            eventInstance = eventSerializer.save()
            
            return Response(
                eventInstance.pk, 
                status=status.HTTP_201_CREATED
            )
        
        return Response(eventSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            event = Event.objects.get(
                pk=pk,
                userId = request.user.id
            )
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        color = Color.objects.get_or_create(
            name = request.data.get('color').get('name'),
        )
        
        request.data['color'] = getattr(color[0], 'pk')

        eventSerializer = PutEventSerializer(event, data=request.data)

        if eventSerializer.is_valid():
            eventSerializer.save()
            return Response(eventSerializer.data, status=status.HTTP_200_OK)
        return Response(eventSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        try:
            event = Event.objects.get(id=pk, userId=request.user.id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response(status=status.HTTP_200_OK)
    
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import math

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = datetime.now()
        year = now.year
        month = str(now.month).zfill(2)
        hour = now.hour * 4
        minute = now.minute
        hour += math.floor(minute / 15)

        upcomingEvents = returnUpcomingEvents(now, hour, user.id)
        upcomingEventSerializer = UpcomingEventSerializer(upcomingEvents, many=True)
        
        events = Event.objects.filter(date__year=year, date__month=month, userId=user.id)
        eventSerializer = EventSerializer(events, many=True)
        
        dateObject = {}

        for event in eventSerializer.data:
            
            dayObject = datetime.strptime(event['date'], '%Y-%m-%d')
            formatted_date = dayObject.strftime("%B %d, %Y")
            day = dayObject.day

            if f'd{day}' not in dateObject:
                dateObject[f'd{day}'] = []
            
            event['color'] = {
                'name' : event['color'],
                'pastel': True
            }
            event['date'] = formatted_date
            
            dateObject[f'd{day}'].append(event)

        for event in upcomingEventSerializer.data:
            date = datetime.strptime(event['date'], "%Y-%m-%d").strftime("%B %d, %Y")
            event['date'] = date


        # for date in eventSerializer.data:
        #     if str(date['date']) == f"{year}-{month}-{day}":
        #         date['requested_day'] = True
        #     else:
        #         date['requested_day'] = False

        refresh = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'events': dateObject,
            'upcoming': upcomingEventSerializer.data
        }, status=status.HTTP_200_OK)

class SingupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

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

    def get(self, request, date, start, name):
        filter_condition = Q(userId=request.user.id)

        print('requestuserid,', request.user.id)
        if name == "-" and int(start) == -1 and date == "-":
            return Response([])
       
        
        if name != "-":
            print('filtering name')
            filter_condition &= Q(name__icontains=name)

        if int(start) != -1:
            print('filtering start')
            filter_condition &= Q(start=int(start))

        if date != "-" and is_date(date):
            print('filtering date')
            filter_condition &= Q(date=date)

        events = Event.objects.filter(filter_condition)[:20]
        print('requestuserid,', events)
        eventSerializer = EventSerializer(events, many=True)

        return Response(eventSerializer.data)
    
import os
from base.tasks import send_the_email
class index(APIView):
    permission_classes = [AllowAny]
    def get(req,self):
        send_the_email.delay()
        
        return Response({'msg': 'hi'})
    
    
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

def returnUpcomingEvents(now, hour, id):
    first_condition_events = Event.objects.filter(
        (Q(date=now.date()) & Q(start__gt=hour)),
        userId=id
    ).order_by('start')[:3]
    
    remaining_events = Event.objects.filter(
        Q(date__gt=now.date()),
        userId=id
    ).order_by('date', 'start')[:3 - first_condition_events.count()]

    return list(first_condition_events) + list(remaining_events)

from dateutil.parser import parse

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False