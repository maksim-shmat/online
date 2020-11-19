""" Docs """

from rest_framework import serializers
from ..models import Subject
from ..models import Course
from ..models import Module
from ..models import Content


class ItemRelatedField(serializers.RelatedField):
    """ docs for class """
    def to_representation(self, value):
        return value.render()

class ContentSerializer(serializers.ModelSerializer):
    """ docs for class """
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['order', 'item']


class ModuleSerializer(serializers.ModelSerializer):
    """ docs for class """
    class Meta:
        model = Module
        fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
    """ docs for class """
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug', 'overview',
                  'created', 'owner', 'modules']


class SubjectSerializer(serializers.ModelSerializer):
    """ docs for class """
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    """ docs for class """
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    """ docs for class """
    modules = ModuleWithContentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'slug',
                  'overview', 'created', 'owner', 'modules']
