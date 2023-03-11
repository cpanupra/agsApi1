from django.urls import path
from . import views

urlpatterns = [
    path('Create_User/',views.registerUser.as_view()),
    path('Api/login/',views.loginView.as_view()),
]