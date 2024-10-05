from .serializers import RegisterSerializer,UserSerializer,RingtoneSerializer,RingtoneLanguageSerializer,StateSerializer, CitySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework.views import APIView
from datetime import timedelta, datetime
from rest_framework import status
from django.utils import timezone
from shuffle import models
import random

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'status': status.HTTP_201_CREATED
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


otp_storage = {}
class GenerateOTPView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = get_object_or_404(User, user_phone=phone_number, status=1)
        except User.DoesNotExist:
            return Response({
                "status": 0,
                "detail": "User not found or inactive."
            }, status=404)
        otp = str(random.randint(1000, 9999))
        expiration_time = datetime.now() + timedelta(minutes=5)
        otp_storage[phone_number] = {'otp': otp, 'expires_at': expiration_time}
        return Response({
            "status": 1,
            "message": "OTP generated successfully!",
            "otp": otp,
            "expires_in": expiration_time.strftime('%Y-%m-%d %H:%M:%S')
        }, status=200)
    
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        otp_data = otp_storage.get(phone_number)
        if not otp_data:
            return Response({
                "status": 0,
                "detail": "OTP not found for this phone number. Please request a new OTP."
            }, status=status.HTTP_400_BAD_REQUEST)
        if datetime.now() > otp_data['expires_at']:
            return Response({
                "status": 0,
                "detail": "OTP has expired. Please request a new OTP."
            }, status=status.HTTP_400_BAD_REQUEST)
        if otp != otp_data['otp']:
            return Response({
                "status": 0,
                "detail": "Invalid OTP."
            }, status=status.HTTP_401_UNAUTHORIZED)
        user = get_object_or_404(User, user_phone=phone_number, status=1)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        expiration_time = datetime.fromtimestamp(access_token['exp'])
        user_data = UserSerializer(user).data
        return Response({
            "status": 1,
            "user": user_data,
            'refresh': str(refresh),
            'access': str(access_token),
            'token_expires_in': expiration_time.strftime('%Y-%m-%d %H:%M:%S')
        }, status=status.HTTP_200_OK)


class GetRingtoneLanguages(APIView):
    def get(self, request):
        languages = models.Ringtone_Language.objects.filter(status=1)
        serializer = RingtoneLanguageSerializer(languages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetStatesView(APIView):
    def get(self, request):
        states = models.State.objects.all().order_by('name')  # Fetch all states, ordered by name
        serializer = StateSerializer(states, many=True)
        return Response({'states': serializer.data}, status=status.HTTP_200_OK)

class GetCitiesView(APIView):
    def get(self, request):
        # Optionally filter cities by state_id if provided as query parameter
        state_id = request.query_params.get('state_id')
        if state_id:
            cities = models.City.objects.filter(state_id=state_id).order_by('name')
        else:
            cities = models.City.objects.all().order_by('name')

        serializer = CitySerializer(cities, many=True)
        return Response({'cities': serializer.data}, status=status.HTTP_200_OK)
    


class RingtoneView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            page = request.data.get('page', 1)
            page_limit = request.data.get('page_limit', 20)
            is_hyped = request.data.get('is_hyped', False)
            try:
                user = models.CustomUser.objects.get(id=user_id)
            except models.CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            ringtone_language = user.ringtone_language
            user_dob_year = user.user_dob.year if user.user_dob else None
            is_all = user.is_all
            state = user.state
            city = user.city
            ringtone_queryset = models.Ringtone.objects.filter(status=1)
            if ringtone_language:
                ringtone_queryset = ringtone_queryset.filter(ringtone_language=ringtone_language)
            if user_dob_year:
                ringtone_queryset = ringtone_queryset.filter(ringtone_year=user_dob_year)
            if is_hyped:
                ringtone_queryset = ringtone_queryset.filter(is_hyped=True)
            if not is_all:
                if state:
                    ringtone_queryset = ringtone_queryset.filter(state=state)
                if city:
                    ringtone_queryset = ringtone_queryset.filter(city=city)
            paginator = Paginator(ringtone_queryset, page_limit)
            ringtones = paginator.get_page(page)
            serializer = RingtoneSerializer(ringtones, many=True)
            return Response({ 'ringtones': serializer.data, 'total_pages': paginator.num_pages, 'current_page': ringtones.number }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)