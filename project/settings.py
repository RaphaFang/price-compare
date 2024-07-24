from pathlib import Path
import os

# nano ~/.zshrc
# source ~/.zshrc

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['raphaelfang.com', 'www.raphaelfang.com','127.0.0.1', 'localhost', '52.4.229.207','0.0.0.0']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'rest_framework', # 這是在設定他的回應格式，我要的是json
]

# 這是在設定他的回應格式，我要的是json
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 增的whitenoise 作為靜態文件處理
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        # 'ENGINE': os.getenv('DJANGO_DB_ENGINE', 'django.db.backends.dummy'),  # 默认使用 dummy，如果没有设置环境变量则使用 dummy
        # 'ENGINE': 'django.db.backends.mysql',  # 這邊禁用原先默認的mysqlclient，解決makemigrations的檢查
        'ENGINE': 'django.db.backends.dummy',  # dummy是佔位用的，我實際用的是aiomysql
        # -----------------------------------------
        'HOST': 'database-v5.cxu0oc6yqrfs.us-east-1.rds.amazonaws.com',
        'USER': os.getenv('SQL_USER'),
        'PASSWORD': os.getenv('SQL_PASSWORD'),
        # -----------------------------------------
        # 'HOST':'host.docker.internal',
        # 'USER':os.getenv('SQL_USER_LOCAL'),
        # 'PASSWORD':os.getenv('SQL_PASSWORD_LOCAL'),
        # -----------------------------------------
        'NAME': 'task_db',
        'PORT': '3306',
    }
}
# S3 相關設定
S3_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME')
CLOUDFRONT_DOMAIN = os.getenv('CLOUDFRONT_DOMAIN')
# 圖片格式設定
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True



# 這是掛載css js的地方，不會影響到admin的 static讀取
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# 嘗試這個

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 設置logger的層級，監聽全部的log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        '__name__': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
