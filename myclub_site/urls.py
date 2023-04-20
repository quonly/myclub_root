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
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView,RedirectView
from events.views import TemplateViewDemo
from . import contact
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

# admin.site.site_header = 'MyClub Administration'
# admin.site.site_title = 'MyClub Site Admin'
# admin.site.index_title = 'MyClub Site Admin Home'

urlpatterns = [
    path('home/',RedirectView.as_view(url='/',permanent=True)),
    path('cbvdemo/',TemplateViewDemo.as_view(template_name='events/cbv_demo.html')),
    path('admin/', admin.site.urls),
    path('admin/password_reset/',auth_views.PasswordResetView.as_view(),name='admin_password_reset'),
    path('admin/password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    path('', include('events.urls')),
    path('contact/',contact.ContactUs.as_view(),name='contact'),
    # path('contact/',contact.contact,name='contact'),
]
