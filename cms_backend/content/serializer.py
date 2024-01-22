import mimetypes
from rest_framework import serializers

from content.models import Category, ContentItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ContentItemSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, required=False, many=True)

    class Meta:
        model = ContentItem
        fields = ('id', 'title', 'body', 'summary',
                  'document', 'categories', 'author')
        extra_kwargs = {'author': {'read_only': True}}

    def validate_document(self, value):
        file_mime_type = mimetypes.guess_type(value.name)[0]
        if file_mime_type != 'application/pdf':
            raise serializers.ValidationError(
                "Only PDF documents are allowed.")
        return value


class ContentItemSearchSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = ContentItem
        fields = ['id', 'author', 'title', 'body', 'summary',
                  'document', 'categories', 'created_at', 'updated_at']
