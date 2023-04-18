from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from datetime import date
import calendar
from calendar import HTMLCalendar
from django.template.response import TemplateResponse
import csv

# gen PDF
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import Event, Venue
from .forms import VenueForm


def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter,bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica-Oblique",14)
    lines = [
        "I will not expose the ignorance of the faculty.",
        "I will not conduct my own fire drills.",
        "I will not prescribe medication.",
    ]
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf,as_attachment=True,filename='bart.pdf')
    
def gen_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="bart.txt"'
    lines = [
        "I will not expose the ignorance of the faculty.\n",
        "I will not conduct my own fire drills.\n",
        "I will not prescribe medication.\n",
    ]
    response.writelines(lines)
    return response
    
def gen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="venues.csv"'
    writer = csv.writer(response)
    venues = Venue.venues.all()
    writer.writerow(['Venue Name','Address','Phone','Email'])
    for venue in venues:
        writer.writerow([venue.name,venue.address,venue.phone,venue.email_address])
    return response
    
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