from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar

from .models import Event


def all_events(request):
    event_list = Event.objects.all()
    context = {
        'event_list': event_list,
    }
    return render(request, 'events/event_list.html', context=context)


def index(request, year=date.today().year, month=date.today().month):
    year = int(year)
    month = int(month)
    if year < 2000 or year > 2099:
        year = date.today().year
    month_name = calendar.month_name[month]
    title = "MyClub Event Calendar - {} {} ".format(month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
    # return HttpResponse("<h1>{}</h1><p>{}</p>".format(title,cal))
    context = {
        'title': title,
        'cal': cal,
    }
    '''
    Render:
        Django first must load the template, create a
        context—which is a dictionary of variables and associated data passed back to the
        browser—and return an HttpResponse.
    '''
    return render(request, 'events/calendar_base.html', context=context)
