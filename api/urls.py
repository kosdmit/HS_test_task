from django.urls import path

from api.views import ProfileView, AuthenticationView

urlpatterns = [
    path('auth/', AuthenticationView.as_view(), name='authentication'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
