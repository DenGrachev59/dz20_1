from django.urls import path


from blog.views import PublicCreateView, PublicListView, PublicDetailView, PublicUpdateView, PublicDeleteView

from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [

    path('create/', PublicCreateView.as_view(), name='create'),
    path('/list_blog/',PublicListView.as_view(), name='list'),
    path('view_blog/<int:pk>', PublicDetailView.as_view(), name='view'),
    path('edit_blog/<int:pk>', PublicUpdateView.as_view(), name='edit'),
    path('delete_blog/<int:pk>', PublicDeleteView.as_view(), name='delete'),

]