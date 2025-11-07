import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# ⚙️ CONFIGURAÇÕES GERAIS
# ==========================

SECRET_KEY = 'django-insecure-substitua-por-uma-chave-secreta-real'
DEBUG = True  # Em produção, defina como False

ALLOWED_HOSTS = ['*']  # coloque seu domínio ou IP em produção

# ==========================
# 🧩 APLICATIVOS INSTALADOS
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seu app local
    'pncpApi',  # troque pelo nome do seu aplicativo
]

# ==========================
# 🔌 MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================
# 📍 ROOT CONFIG
# ==========================
ROOT_URLCONF = 'meuprojeto.urls'

# ==========================
# 🎨 TEMPLATES
# ==========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # pasta de templates
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

# ==========================
# 🚀 WSGI
# ==========================
WSGI_APPLICATION = 'meuprojeto.wsgi.application'

# ==========================
# 🗄️ BANCO DE DADOS (PostgreSQL)
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',         # nome do seu banco
        'USER': 'postgres',          # usuário do PostgreSQL
        'PASSWORD': 'postgress',     # senha
        'HOST': 'localhost',         # ou o IP do servidor
        'PORT': '5432',
        'OPTIONS': {
            # Define o schema padrão (equivalente ao @Entity(schema="meu_schema"))
            'options': '-c search_path=comprasmatch'
        },
    }
}

# ==========================
# 🔐 VALIDAÇÃO DE SENHAS
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================
# 🌍 LOCALIZAÇÃO
# ==========================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Boa_Vista'
USE_I18N = True
USE_TZ = True

# ==========================
# 📁 ARQUIVOS ESTÁTICOS
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ==========================
# 📦 ARQUIVOS DE MÍDIA (UPLOADS)
# ==========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================
# 🧱 CONFIGURAÇÕES PADRÃO
# ==========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
