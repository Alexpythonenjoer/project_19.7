from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import PostsList, PostsDetail, PostsCreate, PostsUpdate, PostsDelete
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('news/', cache_page(60*10)(PostsList.as_view()),
   path('<int:pk>', cache_page(300*10)(PostsDetail.as_view()), name='posts_detail'),
   path('create/', PostsCreate.as_view(), name='posts_create'),
   path('<int:pk>/edit/', PostsUpdate.as_view(), name='posts_update'),
   path('<int:pk>/delete/', PostsDelete.as_view(), name='posts_delete'),
   path('articles/create/', PostsCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/,', PostsUpdate.as_view(), name='article_update'),
   path('<int:pk>/delete/', PostsDelete.as_view(), name='article_delete'),
   path('login/', login_required(PostsUpdate.as_view()))),
]
