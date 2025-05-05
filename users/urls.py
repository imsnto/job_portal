from django.urls import path

from .views import home, UserRegistrationView, UserLoginView
urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]