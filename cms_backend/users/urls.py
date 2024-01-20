from django.urls import path
from users.views import *
urlpatterns = [
    path('users/register/',UserRegistrationView.as_view(),name='user-register' ),
    path('users/token/', UserLoginView.as_view(), name='users-login'), # Role based login
    path('admin/users-list/',UsersListView.as_view(),name="users-list"), # Role based list /?role=user&search=email,phone_number
    path('admin/users/block-unblock/<int:pk>/',BlockUnblockUserView.as_view(),name="block-unblock"),
]