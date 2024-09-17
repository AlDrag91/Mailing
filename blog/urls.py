from blog import views
from blog.apps import BlogConfig
from django.urls import path
from django.views.decorators.cache import cache_page
from blog.views import BlogListView, BlogCreateView, BlogDeleteView, BlogUpdateView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', cache_page(10)(BlogListView.as_view()), name='blog'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail')

]
