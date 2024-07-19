from django.urls import path
from . import views
from .views import (
    UserResourceListView,
    ResourceDetailView,
    ResourceDeleteView,
    ResourceUpdateView,
    download_file
)
from . import views as blog_views

urlpatterns = [
    path('', blog_views.home, name='blog-home'),
    path('resource-list/', blog_views.resource_list, name='resource_list'),
    path('resource-upload/', blog_views.upload_resource, name='resource-upload'),
    path('user/<str:username>/', UserResourceListView.as_view(), name='user-resources'),
    path('resource/<int:pk>/', ResourceDetailView.as_view(), name='resource-detail'),
    path('resource/<int:pk>/update/', ResourceUpdateView.as_view(), name='resource-update'),
    path('resource/<int:pk>/delete/', ResourceDeleteView.as_view(), name='resource-delete'),
    path('resource/<int:pk>/download/', download_file, name='download_file'),
    path('about/', blog_views.about, name='blog-about'),
]
