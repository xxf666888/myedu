from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Note, Comment, Progress, Enrollment, Favorite
from .forms import NoteForm, CommentForm
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse

# 修改课程创建部分
COURSE_CATEGORIES = {
    'python': 'Python开发',
    'web': 'Web开发',
    'data': '数据分析',
    'ai': '人工智能',
    'frontend': '前端开发'
}

def course_list(request):
    # 获取所有课程
    courses = Course.objects.all()
    
    # 如果没有课程，创建一些测试课程
    if not courses.exists():
        # 获取或创建一个教师用户
        User = get_user_model()
        teacher, created = User.objects.get_or_create(
            username='teacher',
            defaults={
                'is_staff': True,
                'password': 'teacher123',
            }
        )

        # 创建 Python 课程及其课时
        python_course = Course.objects.create(
            title='Python 编程基础',
            description='适合编程初学者的 Python 入门课程，包含基础语法、数据类型、控制流程等内容。',
            teacher=teacher,
            category=COURSE_CATEGORIES['python'],
            level='beginner'
        )
        
        # 添加 Python 课程的课时
        python_lessons = [
            '第1章：Python介绍与环境搭建',
            '第2章：Python基础语法',
            '第3章：变量与数据类型',
            '第4章：控制流程',
            '第5章：函数与模块',
            '第6章：面向对象编程',
        ]
        for index, title in enumerate(python_lessons, 1):
            Lesson.objects.create(
                course=python_course,
                title=title,
                content=f'{title}的详细内容',
                order=index,
                video_url=None
            )

        # 创建 Django 课程及其课时
        django_course = Course.objects.create(
            title='Django Web 开发实战',
            description='使用 Django 框架开发现代化 Web 应用，从基础到部署的完整教程。',
            teacher=teacher,
            category=COURSE_CATEGORIES['web'],
            level='intermediate'
        )
        
        # 添加 Django 课程的课时
        django_lessons = [
            '第1章：Django框架介绍',
            '第2章：创建第一个Django项目',
            '第3章：Django模型与数据库',
            '第4章：Django视图与URL配置',
            '第5章：Django模板系统',
            '第6章：用户认证与授权',
            '第7章：表单处理与验证',
            '第8章：部署Django应用'
        ]
        for index, title in enumerate(django_lessons, 1):
            Lesson.objects.create(
                course=django_course,
                title=title,
                content=f'{title}的详细内容',
                order=index,
                video_url=None
            )

        # 创建数据分析课程及其课时
        data_course = Course.objects.create(
            title='数据分析入门',
            description='使用 Python 进行数据分析，包括 Pandas、Numpy 等库的使用。',
            teacher=teacher,
            category=COURSE_CATEGORIES['data'],
            level='beginner'
        )
        
        # 添加数据分析课程的课时
        data_lessons = [
            '第1章：数据分析概述',
            '第2章：NumPy基础',
            '第3章：Pandas入门',
            '第4章：数据清洗与预处理',
            '第5章：数据可视化基础',
            '第6章：统计分析基础',
            '第7章：实战案例分析'
        ]
        for index, title in enumerate(data_lessons, 1):
            Lesson.objects.create(
                course=data_course,
                title=title,
                content=f'{title}的详细内容',
                order=index,
                video_url=None
            )

        # 创建高级Web开发课程及其课时
        advanced_web_course = Course.objects.create(
            title='高级 Web 开发',
            description='深入学习现代 Web 开发技术，包括微服务架构、容器化部署、CI/CD、性能优化等高级主题。',
            teacher=teacher,
            category=COURSE_CATEGORIES['web'],
            level='advanced'
        )
        
        # 添加高级Web开发课程的课时
        advanced_web_lessons = [
            '第1章：现代Web架构概述',
            '第2章：RESTful API设计',
            '第3章：微服务架构',
            '第4章：容器化与Docker',
            '第5章：Kubernetes入门',
            '第6章：CI/CD流程',
            '第7章：性能优化',
            '第8章：安全最佳实践',
            '第9章：监控与日志',
            '第10章：高可用架构设计'
        ]
        for index, title in enumerate(advanced_web_lessons, 1):
            Lesson.objects.create(
                course=advanced_web_course,
                title=title,
                content=f'{title}的详细内容',
                order=index,
                video_url=None
            )

        # 重新获取所有课程
        courses = Course.objects.all()

    # 获取分类并排序
    categories = sorted(Course.objects.values_list('category', flat=True).distinct())
    category = request.GET.get('category')
    level = request.GET.get('level')
    search_query = request.GET.get('search')
    
    if category:
        courses = courses.filter(category__iexact=category)  # 使用 iexact 进行不区分大小写的精确匹配
    if level:
        courses = courses.filter(level=level)
    if search_query:
        courses = courses.filter(title__icontains=search_query) | \
                 courses.filter(description__icontains=search_query)
        
    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'categories': categories,
        'current_category': category,
        'current_level': level,
        'search_query': search_query,
    })

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    is_favorited = Favorite.objects.filter(user=request.user, course=course).exists()
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'is_favorited': is_favorited,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # 检查是否已报名
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, '请先报名课程')
        return redirect('courses:course_detail', course_id=course.id)
    
    # 获取或创建笔记
    note, created = Note.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'content': ''}
    )

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, '笔记已保存！')
            return redirect('courses:lesson_detail', lesson_id=lesson_id)
    else:
        form = NoteForm(instance=note)

    # 获取课程的所有课时
    lessons = course.lessons.all()
    current_lesson_index = list(lessons).index(lesson)
    
    # 获取上一课和下一课
    previous_lesson = lessons[current_lesson_index - 1] if current_lesson_index > 0 else None
    next_lesson = lessons[current_lesson_index + 1] if current_lesson_index < len(lessons) - 1 else None
    
    context = {
        'lesson': lesson,
        'lessons': lessons,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'note_form': form,
        'note': note,
    }
    return render(request, 'courses/lesson_detail.html', context)

@login_required
def save_progress(request, lesson_id):
    if request.method == 'POST':
        lesson = get_object_or_404(Lesson, id=lesson_id)
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        progress.completed = True
        progress.save()
        messages.success(request, '进度已保存！')
    return redirect('courses:lesson_detail', lesson_id=lesson_id)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created:
            messages.success(request, "成功报名课程！")
        else:
            messages.info(request, "您已经报名过这个课程了")
    return redirect('courses:course_detail', course_id=course_id)

@login_required
def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    favorite = Favorite.objects.filter(user=request.user, course=course).first()
    
    if favorite:
        favorite.delete()
        messages.success(request, "已取消收藏")
    else:
        Favorite.objects.create(user=request.user, course=course)
        messages.success(request, "已添加到收藏")
    
    return redirect('courses:course_detail', course_id=course_id)

@login_required
def my_courses(request):
    enrolled_courses = Course.objects.filter(enrollments__user=request.user)
    
    # 计算每个课程的进度
    courses_with_progress = []
    for course in enrolled_courses:
        completed_lessons = Progress.objects.filter(
            user=request.user,
            lesson__course=course,
            completed=True
        ).count()
        total_lessons = course.lessons.count()
        progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
        courses_with_progress.append({
            'course': course,
            'completed_lessons': completed_lessons,
            'total_lessons': total_lessons,
            'progress_percentage': progress_percentage
        })

    return render(request, 'courses/my_courses.html', {
        'courses_with_progress': courses_with_progress
    })

@login_required
def my_favorites(request):
    favorite_courses = Course.objects.filter(favorites__user=request.user)
    return render(request, 'courses/my_favorites.html', {
        'favorite_courses': favorite_courses
    })

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    if request.method == 'POST':
        # 删除学习进度和报名记录
        Progress.objects.filter(user=request.user, lesson__course=course).delete()
        enrollment.delete()
        messages.success(request, "已取消学习该课程")
    
    return redirect('courses:course_list')

@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            note.content = content
            note.save()
            messages.success(request, '笔记已更新！')
            return redirect('courses:my_notes')
    
    return JsonResponse({'content': note.content})

@login_required
def my_notes(request):
    notes = Note.objects.filter(user=request.user).select_related('lesson', 'lesson__course')
    
    # 修改这部分，删除 status 字段的过滤
    enrolled_courses = Course.objects.filter(
        enrollments__user=request.user
    ).distinct()
    
    # 添加调试打印
    print("当前用户:", request.user.username)
    print("已报名课程:", [f"{course.id}: {course.title}" for course in enrolled_courses])
    
    if request.method == 'POST':
        course_id = request.POST.get('course')
        lesson_id = request.POST.get('lesson')
        content = request.POST.get('content')
        
        print("POST数据:", {
            'course_id': course_id,
            'lesson_id': lesson_id,
            'content': content
        })
        
        if course_id and lesson_id and content:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            Note.objects.create(
                user=request.user,
                lesson=lesson,
                content=content
            )
            messages.success(request, '笔记添加成功！')
            return redirect('courses:my_notes')
    
    return render(request, 'courses/my_notes.html', {
        'notes': notes,
        'courses': enrolled_courses,
    })

@login_required
def get_lessons(request, course_id):
    lessons = Lesson.objects.filter(course_id=course_id).values('id', 'title')
    # 添加调试信息
    print(f"获取课程 {course_id} 的课时:", list(lessons))
    return JsonResponse(list(lessons), safe=False)

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, '笔记已删除')
    return redirect('courses:my_notes')

@login_required
def favorites(request):
    favorite_courses = Course.objects.filter(favorites__user=request.user)
    return render(request, 'courses/favorites.html', {
        'favorite_courses': favorite_courses
    })

def health_check(request):
    return HttpResponse("OK")

@login_required
def start_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # 只创建或获取用户的学习进度
    progress, created = Progress.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    return redirect('course_detail', course_id=course_id) 
