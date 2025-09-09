from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('users/new', views.new_user, name="user_new"),
    path('users/<int:pk>/toggle-staff', views.toggle_user_staff, name="user_toggle_staff"),
    path('users/<int:pk>/edit', views.edit_user, name="user_edit"),
    path('users/<int:pk>/delete', views.delete_user, name="user_delete"),
    path('users/<int:pk>/toggle-staff', views.toggle_user_staff, name="user_toggle_staff"),
    path('users/<int:pk>/toggle-superuser', views.toggle_user_superuser, name="user_toggle_superuser"),
    path('clients/new', views.new_client, name="client_new"),
    path('clients/<int:pk>/edit', views.edit_client, name="client_edit"),
    path('clients/<int:pk>/delete', views.delete_client, name="client_delete"),
    path('projects/new', views.new_project, name="project_new"),
    path('tasks/new', views.new_task, name="task_new"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_user, name="logout"),
    #path('store', views.store, name="store"),
]
