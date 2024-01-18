from django.urls import path
from users.views import *
urlpatterns = [
    path('users/register/',UserRegistrationView.as_view,name='user-register' ),
]