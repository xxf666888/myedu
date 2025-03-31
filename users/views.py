from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileEditForm
from courses.models import Course, Enrollment, Favorite, Progress

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('courses:course_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # 获取用户的学习统计
    enrolled_courses = Course.objects.filter(enrollments__user=request.user)
    completed_lessons = Progress.objects.filter(user=request.user, completed=True).count()
    
    context = {
        'enrolled_count': enrolled_courses.count(),
        'completed_lessons': completed_lessons,
        'enrolled_courses': enrolled_courses[:3],  # 最近3个报名的课程
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息更新成功！')
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form}) 