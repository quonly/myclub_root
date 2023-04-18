"""
URL configuration for myclub_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

'''
    There are five different path converter types:
    1. str—matches any non-empty string, excluding ‘/’.
    2. path—matches any non-empty string, including ‘/’ Useful for matching the
    entire URL.
    3. int—matches an integer.
    4. slug—matches any slug string. e.g., slugs-are-text-strings-with-
    hyphens-and_underscores.
    5. UUID—matches a universally unique identifier (UUID).
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
]
