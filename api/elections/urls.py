from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_all_elections),
    path('ongoing/', views.list_ongoing_elections),
    path('expired/', views.list_expired_elections),
    path('vote/<int:candidate_id>/', views.cast_vote),
    path('active/count/', views.active_election_count, name='active_election_count'),
]
