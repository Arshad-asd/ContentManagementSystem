import mimetypes
from rest_framework import serializers

from content.models import Category, ContentItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ContentItemSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(write_only=True)

    class Meta:
        model = ContentItem
        fields = ('id', 'title', 'body', 'summary',
                  'document', 'categories', 'author')
        extra_kwargs = {'categories': {'required': False, 'write_only': True},
                        'author': {'read_only': True, 'required': False}}

    def validate_document(self, value):
        file_mime_type = mimetypes.guess_type(value.name)[0]
        if file_mime_type != 'application/pdf':
            raise serializers.ValidationError(
                "Only PDF documents are allowed.")
        return value

    # def create(self, validated_data):
    #     categories_data = validated_data.pop('categories', [])
    #     content_item = super(ContentItemSerializer, self).create(validated_data)
    #     content_item.categories.set(categories_data)
    #     return content_item


class ContentItemSearchSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = ContentItem
        fields = ['id', 'author', 'title', 'body', 'summary',
                  'document', 'categories', 'created_at', 'updated_at']
