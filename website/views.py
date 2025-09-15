from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm, LoginForm, ClientForm, UserEditForm, UserProfileForm, AdminCreateUserForm, RecordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .models import Client, AccessRequest, Record

# Create your views here.
def home(request):
    return render(request, 'pages/index.html')

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff:
        # Show access request page instead of redirect
        existing = AccessRequest.objects.filter(user=request.user, status=AccessRequest.STATUS_PENDING).first()
        return render(request, 'pages/dashboard_request.html', {
            'has_pending': bool(existing),
            'pending_request': existing,
        })
    users = User.objects.all().order_by('-date_joined')
    # Show all clients and records so you can manage any of them
    clients = Client.objects.all().order_by('-created_at')
    records = Record.objects.all().order_by('-created_at')
    stats = [
        {"label": "Total Users", "value": users.count()},
        {"label": "Your Clients", "value": clients.count()},
        {"label": "Total Records", "value": records.count()},
    ]
    recent = [
        {"title": f"Newest user: {u.username}", "time": u.date_joined.strftime('%Y-%m-%d')} for u in users[:3]
    ]
    context = {
        'stats': stats,
        'recent': recent,
        'users': users,
        'clients': clients,
        'records': records,
    }
    if request.user.is_superuser:
        pending_access = AccessRequest.objects.filter(status=AccessRequest.STATUS_PENDING)
        context['pending_access'] = pending_access
        context['pending_access_count'] = pending_access.count()
    return render(request, 'pages/dashboard.html', context)

@login_required(login_url='login')
def new_project(request):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        desc = (request.POST.get('description') or '').strip()
        if name:
            messages.success(request, f'Project "{name}" created (demo).')
            return redirect('dashboard')
        messages.error(request, 'Please enter a project name.')
    return render(request, 'pages/new_project.html')

@login_required(login_url='login')
def new_task(request):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
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
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    FormClass = AdminCreateUserForm if request.user.is_staff else CreateUserForm
    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            # Save without commit to set role flags safely
            user = form.save(commit=False)
            # Staff flag already applied in AdminCreateUserForm.save(commit=False) if used
            # Superuser flag: only allow superusers to set it
            if hasattr(form, 'cleaned_data') and 'is_superuser' in form.cleaned_data and request.user.is_superuser:
                user.is_superuser = form.cleaned_data.get('is_superuser') or False
            else:
                user.is_superuser = False
            user.save()
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('dashboard')
    else:
        form = FormClass()
    return render(request, 'pages/new_user.html', { 'form': form })

@login_required(login_url='login')
def new_client(request):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
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
def new_record(request):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            rec = form.save(commit=False)
            rec.created_by = request.user
            rec.save()
            messages.success(request, f'Record "{rec.title}" added.')
            return redirect('dashboard')
    else:
        form = RecordForm()
    return render(request, 'pages/new_record.html', { 'form': form })

@login_required(login_url='login')
def edit_client(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    # Allow editing any client
    client = get_object_or_404(Client, pk=pk)
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
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    # Allow deleting any client
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Client "{name}" removed.')
        return redirect('dashboard')
    return render(request, 'pages/delete_client.html', { 'client': client })

@login_required(login_url='login')
def delete_record(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    rec = get_object_or_404(Record, pk=pk)
    if request.method == 'POST':
        title = rec.title
        rec.delete()
        messages.success(request, f'Record "{title}" removed.')
        return redirect('dashboard')
    return render(request, 'pages/delete_record.html', { 'record': rec })

@login_required(login_url='login')
def edit_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    usr = get_object_or_404(User, pk=pk)
    # Allow any logged-in user to edit any user; staff see staff field, others don't
    FormClass = UserEditForm if request.user.is_staff else UserProfileForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=usr)
        if form.is_valid():
            form.save()
            # Ensure superusers remain staff for consistent permissions
            usr.refresh_from_db()
            if usr.is_superuser and not usr.is_staff:
                usr.is_staff = True
                usr.save(update_fields=["is_staff"])
            messages.success(request, f'User "{usr.username}" updated.')
            return redirect('dashboard')
    else:
        form = FormClass(instance=usr)
    return render(request, 'pages/edit_user.html', { 'form': form, 'usr': usr })

@login_required(login_url='login')
def delete_user(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'This action is restricted to staff users.')
        return redirect('home')
    usr = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = usr.username
        # Protect superusers from admin deletion and prevent deleting the last superuser
        if usr.is_superuser:
            if not request.user.is_superuser:
                messages.error(request, 'Only superusers can delete superusers.')
                return redirect('dashboard')
            has_other_su = User.objects.filter(is_superuser=True).exclude(pk=usr.pk).exists()
            if not has_other_su:
                messages.error(request, 'Cannot delete the last superuser.')
                return redirect('dashboard')
        usr.delete()
        if usr == request.user or username == request.user.username:
            messages.success(request, 'Your account was deleted. You have been logged out.')
            logout(request)
            return redirect('login')
        else:
            messages.success(request, f'User "{username}" removed.')
            return redirect('dashboard')
    return render(request, 'pages/delete_user.html', { 'usr': usr })

@login_required(login_url='login')
def request_dashboard_access(request):
    # Allow any authenticated user to request access
    if request.user.is_staff:
        return redirect('dashboard')
    ar = AccessRequest.objects.filter(user=request.user, status=AccessRequest.STATUS_PENDING).first()
    if not ar:
        ar = AccessRequest.objects.create(user=request.user, status=AccessRequest.STATUS_PENDING)
        messages.info(request, 'Access request submitted. An admin will review it shortly.')
    return redirect('dashboard')

@login_required(login_url='login')
def approve_access_request(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can approve access requests.')
        return redirect('dashboard')
    ar = get_object_or_404(AccessRequest, pk=pk, status=AccessRequest.STATUS_PENDING)
    u = ar.user
    u.is_staff = True
    u.save(update_fields=['is_staff'])
    ar.status = AccessRequest.STATUS_APPROVED
    from django.utils import timezone
    ar.responded_at = timezone.now()
    ar.save(update_fields=['status','responded_at'])
    messages.success(request, f'Granted dashboard access to {u.username}.')
    return redirect('dashboard')

@login_required(login_url='login')
def deny_access_request(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can deny access requests.')
        return redirect('dashboard')
    ar = get_object_or_404(AccessRequest, pk=pk, status=AccessRequest.STATUS_PENDING)
    from django.utils import timezone
    ar.status = AccessRequest.STATUS_DENIED
    ar.responded_at = timezone.now()
    ar.save(update_fields=['status','responded_at'])
    messages.info(request, f'Denied dashboard access for {ar.user.username}.')
    return redirect('dashboard')

@login_required(login_url='login')
def toggle_user_staff(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    # Only staff or superuser may toggle staff (and require staff access to dashboard)
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to change staff status.')
        return redirect('dashboard')
    usr = get_object_or_404(User, pk=pk)
    values = request.POST.getlist('is_staff')
    new_is_staff = '1' in values
    was_staff = usr.is_staff
    # Staff cannot change staff flag for superusers
    if request.user.is_staff and not request.user.is_superuser and usr.is_superuser:
        messages.error(request, 'Admins cannot modify superuser roles.')
        return redirect('dashboard')
    usr.is_staff = new_is_staff
    usr.save()
    if usr == request.user and getattr(settings, 'DASHBOARD_STAFF_ONLY', False) and was_staff and not new_is_staff:
        messages.info(request, 'You removed your own staff access. Dashboard is staff-only; you have been redirected.')
        return redirect('home')
    messages.success(request, f'Updated staff status for "{usr.username}" to {"staff" if new_is_staff else "non-staff"}.')
    return redirect('dashboard')

@login_required(login_url='login')
def toggle_user_superuser(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')
    # Only superusers may toggle superuser
    if not request.user.is_superuser:
        messages.error(request, 'Only superusers can change superuser status.')
        return redirect('dashboard')
    usr = get_object_or_404(User, pk=pk)
    values = request.POST.getlist('is_superuser')
    new_is_su = '1' in values
    # Prevent removing last superuser
    if usr.is_superuser and not new_is_su:
        others = User.objects.filter(is_superuser=True).exclude(pk=usr.pk).exists()
        if not others:
            messages.error(request, 'Cannot remove superuser status from the last superuser.')
            return redirect('dashboard')
    usr.is_superuser = new_is_su
    usr.is_staff = usr.is_staff or new_is_su  # superusers are implicitly staff
    usr.save()
    # If self-demoted from superuser and dashboard is staff-only, still allowed as staff
    messages.success(request, f'Updated superuser status for "{usr.username}" to {"superuser" if new_is_su else "standard"}.')
    return redirect('dashboard')

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
