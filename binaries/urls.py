from django.urls import path

from .views import BinaryView, CustomAuthToken

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)


urlpatterns = [
    path('binaries/', BinaryView.as_view()),
    path('token-auth/', CustomAuthToken.as_view())
]

