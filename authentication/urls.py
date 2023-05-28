from django.urls import path

from authentication.views import CustomAuthToken

urlpatterns = [
    path('get-token/', CustomAuthToken.as_view()),
]
