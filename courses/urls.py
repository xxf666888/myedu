from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lesson/<int:lesson_id>/progress/', views.save_progress, name='save_progress'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('my-notes/', views.my_notes, name='my_notes'),
    path('course/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('get-lessons/<int:course_id>/', views.get_lessons, name='get_lessons'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('note/<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('favorites/', views.favorites, name='favorites'),
] 