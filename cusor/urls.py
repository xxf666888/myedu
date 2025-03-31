from django.urls import path
from . import views

urlpatterns = [
    # ... 其他 URL 配置 ...
    path('health/', views.health_check, name='health_check'),
] 