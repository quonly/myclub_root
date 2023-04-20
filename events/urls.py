from django.urls import path, re_path
from django.views.generic.dates import ArchiveIndexView
from .models import Event

from events.admin import admin_site
from . import views
from .views import ListViewDemo, DetailViewDemo, CreateViewDemo,UpdateViewDemo,DeleteViewDemo,ArchiveIndexViewDemo,MonthArchiveViewDemo

urlpatterns = [
    # path('<int:year>/<str:month>/',views.index,name='index'),
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/',MonthArchiveViewDemo.as_view()),
    path('eventarchive/',ArchiveIndexViewDemo.as_view()),
    # path('eventarchive/',ArchiveIndexView.as_view(model=Event,date_field="event_date")),
    path('eventsadmin/', admin_site.urls),
    path('condemo/', views.context_demo, name='condemo'),
    path('tdemo/', views.template_demo, name='tdemo'),
    path('getsubs/', views.list_subscribers, name='list-subscribers'),
    path('gentext/', views.gen_text, name='generate-text-file'),
    path('gencsv/', views.gen_csv, name='generate-csv-file'),
    path('genpdf/', views.gen_pdf, name='generate-pdf-file'),
    path('add_venue/', views.add_venue, name='add-venue'),
    # path('events/',views.all_events,name='show-events'),
    path('events/', ListViewDemo.as_view(), name='show-events'),
    path('event/add/', CreateViewDemo.as_view(), name='add-event'),
    path('event/update/<int:pk>', UpdateViewDemo.as_view(), name='update-event'),
    path('event/delete/<int:pk>', DeleteViewDemo.as_view(), name='delete-event'),
    path('event/<int:pk>', DetailViewDemo.as_view(), name='event-detail'),
    re_path(
        r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
]
