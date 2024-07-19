from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()

            selected_subjects = form.cleaned_data.get('subjects')
            role_group = form.cleaned_data.get('role')
            
            user.groups.clear()
            
            if role_group:
                role_group_obj, created = Group.objects.get_or_create(name=role_group)
                user.groups.add(role_group_obj)
            
            for subject in selected_subjects:
                subject_group, created = Group.objects.get_or_create(name=subject)
                user.groups.add(subject_group)

            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)

    role_group = request.user.groups.filter(name__in=  ['tutor', 'tutee']).first()

    context = {
        'form': form,
        'role_group': role_group,
    }

    return render(request, 'users/profile.html', context)

def custom_logout(request):
    logout(request)
    return render(request, 'users/logout.html')


def tutor_list(request):
    search_query = request.GET.get('q')
    subject_filter = request.GET.get('subject')

    try:
        tutor_group = Group.objects.get(name='tutor')
        tutors = User.objects.filter(groups=tutor_group)
    except Group.DoesNotExist:
        tutors = User.objects.none()

    if search_query:
        tutors = tutors.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if subject_filter:
        tutors = tutors.filter(groups__name=subject_filter)

    subjects = [
        ('MATH 31.1', 'MATH 31.1'),
        ('LAS 21', 'LAS 21'),
        ('MATH 31.2', 'MATH 31.2'),
        ('DECSC 22', 'DECSC 22'),
        ('ITMGT 25.03', 'ITMGT 25.03'),
        ('MATH 31.3', 'MATH 31.3'),
        ('ACCT 115', 'ACCT 115'),
        ('LLAW 113', 'LLAW 113'),
        ('MATH 70.1', 'MATH 70.1'),
        ('ECON 110', 'ECON 110'),
        ('ACCT 125', 'ACCT 125'),
        ('LLAW 115', 'LLAW 115'),
        ('MATH 61.2', 'MATH 61.2'),
        ('DECSC 25', 'DECSC 25'),
        ('ECON 121', 'ECON 121'),
        ('FINN 115', 'FINN 115'),
        ('QUANT 121', 'QUANT 121'),
        ('QUANT 162', 'QUANT 162'),
        ('LAS 111', 'LAS 111'),
        ('MKTG 111', 'MKTG 111'),
        ('QUANT 163', 'QUANT 163'),
        ('LAS 123', 'LAS 123'),
        ('QUANT 192', 'QUANT 192'),
        ('LAS 120', 'LAS 120'),
        ('LAS 140', 'LAS 140'),
        ('OPMAN 125', 'OPMAN 125'),
        ('QUANT 164', 'QUANT 164'),
        ('QUANT 199', 'QUANT 199'),
        ('LAS 197.10', 'LAS 197.10'),
    ]

    subjects = [(code, name) for code, name in subjects if code != 'tutor']

    context = {
        'tutors': tutors,
        'subjects': subjects,
        'selected_subject': subject_filter,
    }
    return render(request, 'users/tutor_list.html', context) 