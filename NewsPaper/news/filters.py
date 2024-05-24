from django_filters import FilterSet
from .models import Posts


class PostsFilter(FilterSet):
   class Meta:
       model = Posts
       fields = {
           'title': ['icontains'],
           'author_name': ['icontains'],
           'date': [
               'lt',
               'gt',
           ],
       }