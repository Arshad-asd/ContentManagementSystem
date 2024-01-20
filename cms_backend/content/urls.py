from django.urls import path
from content.views import *
urlpatterns = [
    path('category/create/',CategoryCreateView.as_view(),name='category-create' ),
    path('create/', ContentItemCreate.as_view(), name='content-create'), 
    path('search/', ContentItemSearchView.as_view(), name='contentitem-search'),
    path('contents-list/',ContentItemListView.as_view(),name='contents-list'),
    path('author/contents-list/',AuthorContentItemList.as_view(),name="author-content-list"),
    path('admin/delete/<int:pk>/',ContentItemDeleteView.as_view(),name="content-delete"),
    path('author/delete/<int:pk>/',AuthorContentItemDeleteView.as_view(),name='author-content-delete'),

]