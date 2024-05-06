from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from datetime import timedelta
from django.utils import timezone
from django.db.models import F
from django.http import JsonResponse
from django.contrib.auth.models import Group
from .forms import *
from django.urls import reverse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import urllib
import io
import os


def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_team_lead(user):
    return user.groups.filter(name='Team_lead').exists()

def is_team_member(user):
    return user.groups.filter(name='Team_member').exists()

def has_admin_or_team_lead_permission(user):
    return user.is_authenticated and (is_admin(user) or is_team_lead(user))


def login_page(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect(reverse("admin_home"))
        elif is_team_lead(request.user):
            return redirect(reverse("team_lead_home"))
        elif is_team_member(request.user):
            return redirect(reverse("team_member_home"))
        else:
            return redirect(reverse("default_home"))
    return render(request, 'registration/login.html')


def admin_home(request):
    return render(request, 'admin_view/dashboard.html')


@login_required(login_url='/login')
# @user_passes_test(has_admin_or_team_lead_permission)
def home(request):
    if request.user.is_authenticated:
        if has_admin_or_team_lead_permission(request.user):
            assigned_tasks = Task.objects.filter(assigned_to=request.user).values()
            latest_assigned_task = Task.objects.filter(assigned_to=request.user).order_by('-id').first()
            deadline_list = Task.objects.filter(assigned_to=request.user).values_list('deadline', flat=True)

            closest_deadline = None
            current_date = timezone.now().date()
            for deadline in deadline_list:
                if closest_deadline is None or (deadline > current_date and deadline < closest_deadline):
                    closest_deadline = deadline

            task_with_closest_deadline = Task.objects.filter(assigned_to=request.user, deadline=closest_deadline).first()

            tasks_passed_deadline = assigned_tasks.filter(deadline__lt=current_date).count()

            out_of = Task.objects.all().count()

            active_tasks = Task.objects.filter(status='in_progress').count()

            completed_tasks = Task.objects.filter(status='completed').count()

            medium = Task.objects.filter(incident_types='medium').count()
            high = Task.objects.filter(incident_types='high').count()
            critical = Task.objects.filter(incident_types='critical').count()

            incident_type = {
                'medium': medium,
                'high': high,
                'critical': critical
            }

            user_roles = {
                'is_admin': is_admin(request.user),
                'is_team_lead': is_team_lead(request.user),
                'is_team_member': is_team_member(request.user),
            }

            pending_count = Task.objects.filter(status='pending').count()
            in_progress_count = Task.objects.filter(status='in_progress').count()
            completed_count = Task.objects.filter(status='completed').count()
            labels = ['Pending', 'In Progress', 'Completed']
            data = [pending_count, in_progress_count, completed_count]
            labels1 = ['Medium', 'High', 'Critical']
            data1 = [medium, high, critical]
        elif is_team_member(request.user):
            return redirect(reverse("TM_dashboard"))

    return render(request, 'base.html', {'assigned_tasks': assigned_tasks, 'latest_assigned_task': latest_assigned_task, 'deadline_alert': task_with_closest_deadline, 'user_roles': user_roles, 'tasks_passed_deadline': tasks_passed_deadline, 'active_tasks': active_tasks, 'completed_tasks': completed_tasks, 'out_of': out_of, 'incident_type': incident_type, 'labels': labels, 'data': data, 'labels1': labels1, 'data1': data1})


def user_activity_chart(request, user_id):
    user_activity = UserActivityLog.objects.filter(user_id=user_id)
    
    dates = [log.date for log in user_activity]
    activities = [log.activity for log in user_activity]

    # Create the chart
    plt.plot(dates, activities)
    plt.xlabel('Date')
    plt.ylabel('Activity')
    plt.title('User Activity Chart')
    
    # Save the chart to a file or render it directly in the template
    chart_path = 'path_to_save_chart/chart.png'  # Specify a path to save the chart
    plt.savefig(chart_path)

    return render(request, 'user_activity_chart.html', {'chart_path': chart_path})

def task_status_data(request):
    pending_count = Task.objects.filter(status='pending').count()
    in_progress_count = Task.objects.filter(status='in_progress').count()
    completed_count = Task.objects.filter(status='completed').count()
    
    # Create data for the chart
    labels = ['Pending', 'In Progress', 'Completed']
    data = [pending_count, in_progress_count, completed_count]
    
    
    return render(request, 'base.html', {'labels': labels, 'data': data})

def task_incident_data(request):
    medium = Task.objects.filter(incident_types='medium').count()
    high = Task.objects.filter(incident_types='high').count()
    critical = Task.objects.filter(incident_types='critical').count()
    
    # Create data for the chart
    labels = ['Medium', 'High', 'Critical']
    data = [medium, high, critical]
    
    return render(request, 'base.html', {'labels': label, 'data': data})

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_view.html', {'tasks': tasks})

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'tasks/task_detail.html', {'task': task})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'incident_types', 'assigned_to', 'assigned_team']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'status', 'incident_types']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.created_by or self.request.user == task.assigned_to:
            return True
        return False

def add_team(request):
    # task = get_object_or_404(Task)

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            # team.task = task
            team.save()
            response_data = {
                'team_id': team.pk,
                'status': 'success'
            }
            return JsonResponse(response_data)
    else:
        form = TeamForm()

    return render(request, 'tasks/add_team.html', {'form': form,})


def tm_dashboard(request):
    return render(request, 'TM_view/dashboard.html')

def team(request):
    teams = Team.objects.all()
    return render(request, 'tasks/team.html', {'teams': teams})
