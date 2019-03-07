from django_filters import rest_framework as filters
from django.db import models
from .models import Resume

class Resumefilter(filters.FilterSet):
    class Meta:
        model = Resume
        fields = '__all__'
        filter_overrides = {
            models.FileField: {
                # A FileField or ImageField stores the path of the file or image.
                # At the DB level they are same as a CharField.
                # http://books.agiliq.com/projects/django-orm-cookbook/en/latest/filefield.html
                 'filter_class': filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
        }
