from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('signup/', views.signuppage, name='signup'),
    path('home/', views.homepage, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('post/', views.postpage, name='post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('profile/', views.profilepage, name='profile'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/update/', views.update_post, name='update_post'),
]
