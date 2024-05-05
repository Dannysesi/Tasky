"""
URL configuration for task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from django.contrib.auth import views as auth_views
from project import views as project_views

urlpatterns = [
    # user app url
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', user_view.register, name='register'),
    path('verify-otp/', user_view.verify_otp, name='verify_otp'),
    path('profile/', user_view.profile, name='profile'),

    # project app url
    path('', project_views.home, name='home'),
    path('tasks/', project_views.task_list, name='task'),
    path('task_detail/<int:id>/', project_views.task_detail, name='task_detail'),
    path('task/new/', project_views.TaskCreateView.as_view(template_name='tasks/task_form.html'), name='task-create'),
    path('task/<int:pk>/update/', project_views.TaskUpdateView.as_view(template_name='tasks/task_form.html'), name='task_update'),
    path('task/<int:pk>/delete/', project_views.TaskCreateView.as_view(template_name='tasks/task_form.html'), name='task-delete'),
    # path('add_team/', project_views.add_team, name='add_team'),
    path('add_team/', project_views.add_team, name='add_team'),
    path('team/', project_views.team, name='team'),

    # admin dashboard
    path('admin_home', project_views.admin_home, name='admin_home'),


    # Team member dashboard
    path('TM_dashboard', project_views.tm_dashboard, name='TM_dashboard'),

    # password reset
    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html'),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-comfirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
        name='password_reset_complete'),

    #Chart
    # path('task-status-data/', project_views.task_status_data, name='task_status_data'),
    # path('task-incident-data/', project_views.task_incident_data, name='task_incident_data'),
]
