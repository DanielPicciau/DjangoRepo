from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

@login_required
def dashboard(request):
    # Sample, non-persistent dashboard context (replace with real data later)
    stats = [
        {"label": "Projects", "value": 4, "icon": "bi-kanban"},
        {"label": "Tasks", "value": 18, "icon": "bi-check2-circle"},
        {"label": "Team", "value": 3, "icon": "bi-people"},
    ]
    recent = [
        {"title": "Updated profile settings", "time": "2h ago"},
        {"title": "Created a new task: Wireframe UI", "time": "Yesterday"},
        {"title": "Invited Alex to the project", "time": "2 days ago"},
    ]
    actions = [
        {"label": "New Project", "href": "#", "style": "primary"},
        {"label": "New Task", "href": "#", "style": "outline-primary"},
    ]
    return render(request, 'pages/dashboard.html', {
        'stats': stats,
        'recent': recent,
        'actions': actions,
    })

@login_required
def new_project(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        desc = (request.POST.get('description') or '').strip()
        if name:
            messages.success(request, f'Project "{name}" created (demo).')
            return redirect('dashboard')
        messages.error(request, 'Please enter a project name.')
    return render(request, 'pages/new_project.html')

@login_required
def new_task(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        due = (request.POST.get('due') or '').strip()
        if title:
            messages.success(request, f'Task "{title}" added (demo).')
            return redirect('dashboard')
        messages.error(request, 'Please enter a task title.')
    return render(request, 'pages/new_task.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Add a success message for the user
            messages.success(request, 'Account created successfully! Please log in.')
            # Redirect to the login page after successful registration
            return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form': form}
    return render(request, 'pages/register.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')
