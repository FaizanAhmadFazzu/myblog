from django.urls import path
from django.views.generic.base import RedirectView
from blog import views
urlpatterns = [
    # path('', PostListView.as_view(), name='blog-home'),
    path('home/', views.HomeView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.about, name='blog-contact'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
     path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<category>/', views.blog_category, name='blog_category'),
    path('post/like/<int:pk>', views.like, name='post-like'),
    path('post/unlike/<int:pk>', views.unlike, name='post-unlikelike'),
    path('profile/', views.ProfileListView.as_view(), name='blog-profiles'),
    path('profile/follow/<int:pk>', views.follow, name='follow-user'),
    path('profile/unfollow/<int:pk>', views.unfollow, name='unfollow-user'),
    path('profile/edit/<int:pk>', views.ProfileUpdateView.as_view(success_url="/blog/home"), name='profile-update'),

    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('', RedirectView.as_view(url="home/")),  

]