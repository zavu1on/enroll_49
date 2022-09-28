from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('enroll/', views.EnrollView.as_view()),
    path('profile/', views.ProfileView.as_view()),
]
