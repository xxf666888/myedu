from django.db import models
from users.models import CustomUser

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='课程名称')
    description = models.TextField(verbose_name='课程描述')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_taught', verbose_name='讲师')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails', blank=True, verbose_name='课程封面')
    category = models.CharField(max_length=50, verbose_name='课程分类', default='其他')
    level = models.CharField(max_length=20, choices=[
        ('beginner', '入门'),
        ('intermediate', '中级'),
        ('advanced', '高级')
    ], default='beginner', verbose_name='难度等级')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='所属课程')
    title = models.CharField(max_length=200, verbose_name='课时标题')
    content = models.TextField(verbose_name='课时内容')
    video_url = models.URLField(blank=True, null=True, verbose_name='视频链接', help_text='可选：添加视频链接')
    order = models.IntegerField(default=0, verbose_name='排序')
    duration = models.IntegerField(default=0, verbose_name='时长(分钟)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = '课时'
        verbose_name_plural = '课时'

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    class Meta:
        verbose_name = '课程报名'
        verbose_name_plural = '课程报名'
        unique_together = ['user', 'course']

class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='notes', verbose_name='课时')
    content = models.TextField(verbose_name='笔记内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '学习笔记'
        verbose_name_plural = '学习笔记'
        ordering = ['-updated_at']  # 按更新时间倒序排列

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments', verbose_name='课时')
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = '课程评论'

class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress', verbose_name='用户')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress', verbose_name='课时')
    completed = models.BooleanField(default=False, verbose_name='是否完成')
    last_watched = models.DateTimeField(auto_now=True, verbose_name='最后观看时间')
    watch_duration = models.IntegerField(default=0, verbose_name='观看时长(分钟)')

    class Meta:
        verbose_name = '学习进度'
        verbose_name_plural = '学习进度'

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favorites', verbose_name='课程')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')

    class Meta:
        verbose_name = '课程收藏'
        verbose_name_plural = '课程收藏'
        unique_together = ['user', 'course'] 
