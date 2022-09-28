from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('enroll/', views.EnrollView.as_view(), name='enroll'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
