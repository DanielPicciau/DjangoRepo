from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    #path('store', views.store, name="store"),
]
