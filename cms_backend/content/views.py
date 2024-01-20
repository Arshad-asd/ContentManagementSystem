from content.serializer import *
from content.models import ContentItem, Category
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics
from rest_framework import generics, status
from rest_framework.response import Response


class CategoryCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class ContentItemCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer

    def create(self, request, *args, **kwargs):
        categories_data = request.data.get('categories', '')
        category_names = categories_data.split(',')

        # Convert category names to category IDs
        category_ids = []
        for category_name in category_names:
            # Fetch the corresponding category ID
            category = Category.objects.filter(name=category_name).first()
            if category:
                category_ids.append(category.id)
            else:
                return Response(
                    {"categories": [f"Category '{category_name}' does not exist."]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Remove the existing 'categories' key
        request.data.pop('categories', None)

        # Add the category IDs to the request data
        request.data['categories']=category_ids
        print(category_ids,'kkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
        request.data['author'] = request.user.id
        print(request.user.id,'jjjjjjjjjjjjjjjjjjj')
        print(request.data,'daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # Create the serializer with the updated request data
        serializer = self.get_serializer(data=request.data)
        print(serializer,'ssssssssssssssssssssssssssssssssssss')
        serializer.is_valid(raise_exception=True)

        # Perform the create operation
        self.perform_create(serializer)
        # serializer.instance.categories.set(category_ids)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ContentItemSearchView(generics.ListAPIView):
    serializer_class = ContentItemSearchSerializer

    def get_queryset(self):
        search_terms = self.request.query_params.get('search', '')

        queryset = ContentItem.objects.filter(
            Q(title__icontains=search_terms) |
            Q(body__icontains=search_terms) |
            Q(summary__icontains=search_terms) |
            Q(categories__name__icontains=search_terms)
        ).distinct()

        return queryset


class ContentItemListView(generics.ListAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSearchSerializer

class AuthorContentItemList(generics.ListAPIView):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        author_id = self.request.user.id  # Assuming the author is the currently authenticated user
        return ContentItem.objects.filter(author_id=author_id)

class ContentItemDeleteView(generics.DestroyAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'detail': 'Content deleted'}, status=200)

class AuthorContentItemDeleteView(generics.DestroyAPIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the authenticated user is the author of the content
        if request.user.role == 'author': 
            self.perform_destroy(instance)
            return self.get_response(message="ContentItem deleted successfully.")
        else:
            return self.get_response(message="You are not allowed to delete this ContentItem.", status=403)

    def get_response(self, message, status=200):
        return Response({'detail': message}, status=status)