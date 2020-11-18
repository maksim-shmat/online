""" Let's build the course models. """

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .fields import OrderField


class Subject(models.Model):
    """ This subject options, right? """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return str(self.title)    # add str

    
class Course(models.Model):
    """" - owner: The instructor that created this course.
         - subject: The subject that this course belong to. A ForeignKey
         field that points to the Subject model.
         - title: The title of the course.
         - slug: The slug of the course. This will be used un URLs later.
         - overview: This is a TextField column to include an overview of
         the course.
         - created: The date and time when the course was created. It will
         be automatically set by Django when creating new objects because of
         auto_now_add=True
    """
    owner = models.ForeignKey(User, related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name='courses_joined',
                                      blank=True)


    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    """ Make are windows? """
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    """ Make are more windows? """
    module = models.ForeignKey(Module, related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={'model__in':('text',
                                                                    'video',
                                                                    'image',
                                                                    'file')},
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    """ Make are more windows? """
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
            self._meta.model_name), {'item': self})


class Text(ItemBase):
    """ You will be write this. """
    content = models.TextField()

class File(ItemBase):
    """ Will be add file object. """
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    """ Sould be add picture. """
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    """ Add link from video hosting. """
    url = models.URLField()
