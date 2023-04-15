from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('enroll/', views.EnrollView.as_view(), name='enroll'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),

    path('api/statistic/', views.ListStatisticView.as_view()),
    path('api/profiles/', views.ListProfileClassesView.as_view()),
]
