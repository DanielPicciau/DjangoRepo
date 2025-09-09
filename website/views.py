from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm, ClientForm, UserEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Client

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

@login_required(login_url='login')
def dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    clients = Client.objects.filter(created_by=request.user).order_by('-created_at')
    stats = [
        {"label": "Total Users", "value": users.count()},
        {"label": "Your Clients", "value": clients.count()},
    ]
    recent = [
        {"title": f"Newest user: {u.username}", "time": u.date_joined.strftime('%Y-%m-%d')} for u in users[:3]
    ]
    return render(request, 'pages/dashboard.html', {
        'stats': stats,
        'recent': recent,
        'users': users,
        'clients': clients,
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

@login_required(login_url='login')
def new_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('dashboard')
    else:
        form = CreateUserForm()
    return render(request, 'pages/new_user.html', { 'form': form })

@login_required(login_url='login')
def new_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'Client "{client.name}" added.')
            return redirect('dashboard')
    else:
        form = ClientForm()
    return render(request, 'pages/new_client.html', { 'form': form })

@login_required(login_url='login')
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client "{client.name}" updated.')
            return redirect('dashboard')
    else:
        form = ClientForm(instance=client)
    return render(request, 'pages/edit_client.html', { 'form': form, 'client': client })

@login_required(login_url='login')
def delete_client(request, pk):
    client = get_object_or_404(Client, pk=pk, created_by=request.user)
    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Client "{name}" removed.')
        return redirect('dashboard')
    return render(request, 'pages/delete_client.html', { 'client': client })

@login_required(login_url='login')
def edit_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit users.')
        return redirect('dashboard')
    usr = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=usr)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{usr.username}" updated.')
            return redirect('dashboard')
    else:
        form = UserEditForm(instance=usr)
    return render(request, 'pages/edit_user.html', { 'form': form, 'usr': usr })

@login_required(login_url='login')
def delete_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('dashboard')
    usr = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = usr.username
        # Prevent self-deletion to avoid logging current user out unexpectedly
        if usr == request.user:
            messages.error(request, 'You cannot delete your own account here.')
            return redirect('dashboard')
        usr.delete()
        messages.success(request, f'User "{username}" removed.')
        return redirect('dashboard')
    return render(request, 'pages/delete_user.html', { 'usr': usr })

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
