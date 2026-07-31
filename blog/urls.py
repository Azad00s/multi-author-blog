from django.urls import path
from . import views

app_name = 'blog'   # This allows us to refer to URLs by name, e.g., 'blog:home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('author/<int:user_id>/', views.AuthorProfileView.as_view(), name='author_profile'),
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<slug:slug>/like/', views.LikeToggleView.as_view(), name='like_toggle'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('search/', views.SearchView.as_view(), name='search'),
]