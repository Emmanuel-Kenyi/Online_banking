from django.urls import path
from .import views

urlpatterns = [
    path('user/', views.current_user, name='current-user'),  
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('count/', views.user_count, name='user_count'),

]
