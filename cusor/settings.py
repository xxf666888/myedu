import environ
import os
from pathlib import Path

env = environ.Env()

# 构建基础目录路径
BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# 读取环境变量
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# 数据库配置
DATABASES = {
    'default': env.db('DATABASE_URL')
}

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
