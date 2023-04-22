# django
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import FileResponse
from django.core import serializers
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, get_connection
from django.contrib import messages

# django template,views
from django.template import RequestContext, Template
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.views.generic.dates import ArchiveIndexView, MonthArchiveView
from django.forms import formset_factory, modelformset_factory

# models and forms
from events.models import Venue,MyClubUser,Event
from events.forms import EventForm, CommitteeForm

# python package
from datetime import datetime
import csv
import io

# django app 
from formtools.wizard.views import SessionWizardView

# csv pdf
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# model form wizards

class ModelFormWizard(SessionWizardView):
    template_name = 'events/modelwiz_demo.html'
    def done(self,form_list,**kwargs):
        for form in form_list:
            form.save()
        return redirect('/')

# multi form
'''
ขั้นตอนการสร้าง
    1. สร้างฟอร์มก่อน โดยสืบทอดมาจาก forms.Form ตามปกติและตั้งค่าตามที่ต้องการ
    2. มาที่ views และสร้างคลาสที่สืบทอดมาจาก SessionWizardView ภายในคลาสนี้ต้องการเมธอด done เพื่อจัดการกับฟอร์มที่ทำเสร็จแล้ว 
    3. สร้าง template โดยจะต้องใส่ wizard.management_form ภายใน form ด้วยทุกครั้ง แจงโก้จะทำการเรนเดอร์เป็น input:hidden ใช้เพื่อให้แจงโก้สามารถจัดการกับฟอร์มวิซาร์ดได้
    4. เพิ่มพาธที่ urls เนื่องจากเป็นคลาสวิวจะต้องต่อท้ายด้วยเมธอด as_view([form1,form2]) โดยที่จะต้องใส่ลิสต์ของฟอร์มเข้าไปภายในเมธอดด้วย เพื่อให้รู้ว่าใช้ฟอร์มใดบ้าง
'''

class SurveyWizard(SessionWizardView):
    template_name = 'events/survey.html'
    def done(self,form_list,**kwargs):
        print('form_list',form_list)
        responses = [form.cleaned_data for form in form_list]
        mail_body = ''
        for response in responses:
            print('response.items()',response.items())
            for k,v in response.items():
                mail_body += f"{k}: {v}\n"
        con = get_connection('django.core.mail.backends.console.EmailBackend')
        send_mail(
            'Survey Submission',
            mail_body,
            'noreply@example.com',
            ['siteowner@example.com'],
            connection=con
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Your survey was submitted successfully. Thank you for your feedback'
        )
        return redirect('/survey')

############################################

# formset

def all_events(request):
    EventsFormSet = modelformset_factory(
        Event,
        fields=('name','event_date',),
        extra=0
    )
    qry = Event.events.all()
    pg = Paginator(qry,4)
    page = request.GET.get('page')
    try:
        event_records = pg.page(page)
    except PageNotAnInteger:
        event_records = pg.page(1)
    except EmptyPage:
        event_records = pg.page(pg.num_pages)
    if request.method == 'POST':
        formset = EventsFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return_url = '/allevents'
            if 'page' in request.GET:
                return_url +=f'?page={request.GET["page"]}'
            return redirect(return_url)
    else:
        page_qry = qry.filter(id__in=[event.id for event in event_records])
        print('page_qry',page_qry)
        formset = EventsFormSet(queryset=page_qry)
    context = {'event_records':event_records,'formset':formset}
    return render(request,'events/all_events.html',context)

def committee_formset(request):
    committee_formset = formset_factory(CommitteeForm,extra=3)
    if request.method == 'POST':
        formset = committee_formset(request.POST)
        if formset.is_valid():
            # process the form
            pass
    else:
        formset = committee_formset()
        return render(request,'events/committee.html',{'formset':formset})

###################################################

# Class-Based-Views (CBV)

class MonthArchiveViewDemo(MonthArchiveView):
    queryset = Event.events.all()
    date_field = "event_date"
    context_object_name ='event_list'
    allow_future = True
    month_format = '%m'

class ArchiveIndexViewDemo(ArchiveIndexView):
    model=Event
    date_field="event_date"
    allow_future = True

class DeleteViewDemo(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('show-events')

class UpdateViewDemo(LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    model = Event
    # fields = ['name','event_date','description']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('show-events')
    form_class = EventForm

class CreateViewDemo(LoginRequiredMixin,CreateView):
    # login, logout, register เป็น name URL ที่แจงโก้สร้างไว้ให้อยู่แล้ว
    login_url = reverse_lazy('login')
    model = Event
    # fields = ['name','event_date','description']
    success_url = reverse_lazy('show-events')
    form_class = EventForm

class ListViewDemo(ListView):
    model = Event
    context_object_name = 'all_events'
    # paginate_by = 2 # ทำให้แบ่ง pagination ในคลาสได้
    
class DetailViewDemo(DetailView):
    model = Event
    context_object_name = 'event'

class TemplateViewDemo(TemplateView):
    template_name = "events/cbv_demo.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Testing The TemplateView CBV"
        return context

######################################################################
def my_processor(request):
    return {
        'foo':'foo',
        'bar':'bar',
        'baz':'baz',
    }

def context_demo(request):
    template = Template('{{foo}}<br>{{bar}}<br>{{baz}}<br>{{user}}<br>{{perms}}<br>{{request}}<br>{{messages}}<br>{{LANGUAGE_CODE}}<br>{{LANGUAGE_BIDI}}<br>')
    con = RequestContext(request,processors=[my_processor])
    return HttpResponse(template.render(con))

def gen_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica-Oblique", 14)
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
    return FileResponse(buf, as_attachment=True, filename='bart.pdf')


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
    writer.writerow(['Venue Name', 'Address', 'Phone', 'Email'])
    for venue in venues:
        writer.writerow([venue.name, venue.address,
                        venue.phone, venue.email_address])
    return response


def template_demo(request):
    empty_list = []
    color_list = ['red', 'green', 'blue', 'yellow']
    somevar = 5
    anothervar = 21
    today = datetime.now()
    past = datetime(1985, 11, 5)
    future = datetime(2035, 11, 5)
    best_bands = [
        {'name': 'The Angels', 'country': 'Australia'},
        {'name': 'AC/DC', 'country': 'Australia'},
        {'name': 'Nirvana', 'country': 'USA'},
        {'name': 'The Offspring', 'country': 'USA'},
        {'name': 'Iron Maiden', 'country': 'UK'},
        {'name': 'Rammstein', 'country': 'Germany'},
    ]
    aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
    venues_js = serializers.serialize('json', Venue.venues.all())

    context = {
        'somevar': somevar,
        'anothervar': anothervar,
        'empty_list': empty_list,
        'color_list': color_list,
        'best_bands': best_bands,
        'today': today,
        'past': past,
        'future': future,
        'aussie_bands': aussie_bands,
        'venues': venues_js,
    }

    return render(request, 'events/template_demo.html', context)
