from django.contrib import admin
from .models import Course, Lesson, Note, Comment, Progress, Enrollment, Favorite

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'level', 'created_at')
    list_filter = ('category', 'level')
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    ordering = ('course', 'order')

admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(Progress)
admin.site.register(Enrollment)
admin.site.register(Favorite) 