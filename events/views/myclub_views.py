from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.core.paginator import Paginator

from calendar import HTMLCalendar
from datetime import date
import calendar

from events.models import Event, Venue, MyClubUser
from events.forms import VenueForm
    
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

    announcements = [
        {
            'date':'6-10-2020',
            'announcement': 'Club Registrations Open'
        },
        {
            'date':'6-15-2020',
            'announcement': 'Joe Smith Elected New Club President'
        }
    ]
    
    context = {
        'title': title,
        'cal': cal,
        'announcements':announcements,
    }
    
    '''
    Render:
        Django first must load the template, create a
        context—which is a dictionary of variables and associated data passed back to the
        browser—and return an HttpResponse.
    '''
    # return render(request, 'events/calendar_base.html', context=context)
    return TemplateResponse(request, 'events/calendar_base.html', context=context)


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    
    context = {
        'form':form,
        'submitted': submitted
    }
    
    return render(request,'events/add_venue.html',context)

def list_subscribers(request):
    p = Paginator(MyClubUser.objects.all(),2)
    page = request.GET.get('page')
    subscribers = p.get_page(page)
    context = {
        'subscribers':subscribers
    }
    return render(request,'events/subscribers.html',context)