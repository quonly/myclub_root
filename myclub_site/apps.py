from django.contrib.admin.apps import AdminConfig

class MyClubAdminConfig(AdminConfig):
  default_site = 'myclub_site.admin.MyClubAdmin'