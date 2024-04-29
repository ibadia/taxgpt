from django.urls import path
from apps.user_app.api.views import user_api

urlpatterns = [
	path('register', user_api.UserRegister.as_view(), name='register'),
	path('login', user_api.UserLogin.as_view(), name='login'),
	path('logout', user_api.UserLogout.as_view(), name='logout'),
	path('user', user_api.UserView.as_view(), name='user'),
]