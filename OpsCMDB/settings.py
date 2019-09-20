"""
Django settings for OpsCMDB project.

Generated by 'django-admin startproject' using Django 1.11.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's@9mj49!8dkouv6!g!qwv+==p_5l*&f3b5_8*bp9vo$jpynt5o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'imagekit',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 权限管理
    'rbac',
    # 监控
    "monitor",
    # kafka
    'logpipe'

]

LOGPIPE = {
    # Required Settings
    'OFFSET_BACKEND': 'logpipe.backend.kafka.ModelOffsetStore',
    'CONSUMER_BACKEND': 'logpipe.backend.kafka.Consumer',
    'PRODUCER_BACKEND': 'logpipe.backend.kafka.Producer',
    'KAFKA_BOOTSTRAP_SERVERS': [
        '10.0.7.7:9092'
    ],
    'KAFKA_CONSUMER_KWARGS': {
        'group_id': 'minitor-alert',
    },

    # Optional Settings
    # 'KAFKA_SEND_TIMEOUT': 10,
    # 'KAFKA_MAX_SEND_RETRIES': 0,
    # 'MIN_MESSAGE_LAG_MS': 0,
    # 'DEFAULT_FORMAT': 'json',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'rbac.middlewares.rbac_middle.RbacMiddleware',
]
REX_FORMAT = "^%s$"
VALID_LIST = [
    '/rbac/login.html',
    '/rbac/logout',
    '^/admin/.*',
    '/index/',
]
DEBUG = True

AUTH_USER_MODEL = 'rbac.UserInfo'

ROOT_URLCONF = 'OpsCMDB.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'OpsCMDB.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

cf = configparser.ConfigParser()
cf.read("OpsCMDB/config.ini")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': cf.get("db", "name"),
        'USER': cf.get("db", "user"),
        'PASSWORD': cf.get("db", "pass"),
        'HOST': cf.get("db", "host"),
        'PORT': cf.get("db", "port"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'Zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR + '/static',)
LOGIN_URL = '/rbac/login.html'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_URL = '/upload/'

# #################### 权限相关配置 #############################
PERMISSION_DICT_SESSION_KEY = "user_permission_dict_key"
PERMISSION_MENU_SESSION_KEY = "user_permission_menu_key"

# session 设置
SESSION_COOKIE_AGE = 60 * 30  # 30分钟
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效
# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        # 针对 DEBUG = True 的情况
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 对日志信息进行格式化，每个字段对应了日志格式中的一个字段，更多字段参考官网文档，我认为这些字段比较合适，输出类似于下面的内容
    'formatters': {
        # INFO 2016-09-03 16:25:20,067 /home/ubuntu/mysite/views.py views.py views get 29: some info...
        'standard': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
        # 用于文件输出
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/data/WebHook/log/cmdb.log',
            'formatter': 'standard'
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        # 是否继承父类的log信息
        'django': {
            # handlers 来自于上面的 handlers 定义的内容
            'handlers': ['file_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
