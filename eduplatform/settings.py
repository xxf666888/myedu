import os
from pathlib import Path

# 构建基础目录路径
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses.apps.CoursesConfig',
    'users.apps.UsersConfig',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'users.CustomUser'

# 添加中间件配置
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 添加模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 添加数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 添加密钥配置（这个也是必需的）
SECRET_KEY = 'django-insecure-your-secret-key-here'

# 开启调试模式
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = ['*']

# 添加静态文件配置
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 添加 ROOT_URLCONF 配置
ROOT_URLCONF = 'eduplatform.urls'

# 添加 WSGI 应用配置
WSGI_APPLICATION = 'eduplatform.wsgi.application'

# 添加登录相关的设置
LOGIN_REDIRECT_URL = '/'  # 登录成功后重定向到首页
LOGOUT_REDIRECT_URL = '/'  # 登出后重定向到首页
LOGIN_URL = '/users/login/'  # 登录页面的 URL 
