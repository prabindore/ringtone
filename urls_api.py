from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from shuffle import APIviews

urlpatterns = [
    # Auth endpoints
    path('user/register/', APIviews.RegisterView.as_view(), name='user_register'),
    path('user/login/', APIviews.LoginView.as_view(), name='user_login'),

    path('user/ringtone_languages/', APIviews.GetRingtoneLanguages.as_view(), name='get_ringtone_languages'),
    path('user/get_states/', APIviews.GetStatesView.as_view(), name='get_states'),
    path('user/get_cities/', APIviews.GetCitiesView.as_view(), name='get_cities'),

    path('user/generate_otp/', APIviews.GenerateOTPView.as_view(), name='generate_otp'),
    
    path('user/get_ringtones/', APIviews.RingtoneView.as_view(), name='get_ringtones'),

    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]