from django.urls import path
from users.views import *
from content.views import *
urlpatterns = [
    path('users/register/',UserRegistrationView.as_view(),name='user-register' ),
    path('users/token/', UserLoginView.as_view(), name='users-login'), # Role based login
    path('users/content/search/', ContentItemSearchView.as_view(), name='contentitem-search'),

    path('admin/users-list/',UsersListView.as_view(),name="users-list"), # Role based list /?role=user&search=email,phone_number
    path('admin/users/block-unblock/<int:pk>/',BlockUnblockUserView.as_view(),name="block-unblock"),

    path('admin/category/create/',CategoryCreateView.as_view(),name='category-create' ),
    path('admin/content/contents-list/',ContentItemListView.as_view(),name='contents-list'),
    path('admin/content/delete/<int:pk>/',ContentItemDeleteView.as_view(),name="content-delete"),

    path('author/content/create/', ContentItemCreate.as_view(), name='content-create'), 
    path('author/content/contents-list/',AuthorContentItemList.as_view(),name="author-content-list"),
    path('author/content/delete/<int:pk>/',AuthorContentItemDeleteView.as_view(),name='author-content-delete'),
] 