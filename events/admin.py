from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django import forms

from .models import Event, Venue, MyClubUser
from events.forms import VenueForm
from ckeditor.widgets import CKEditorWidget

from datetime import datetime
import csv

# add actions
def venue_csv(modeladmin,request,queryset):
    response = HttpResponse(content_type='text/csv')
    crr_datetime = datetime.now()
    response['Content-Disposition'] = 'attachment;filename="venue_export{}.csv"'.format(crr_datetime.microsecond)
    writer = csv.writer(response)
    writer.writerow(['name','event_date','venue','descriptoin'])
    for record in queryset:
        rec_list = []
        rec_list.append(record.name)
        rec_list.append(record.event_date.strftime("%m/%d/%Y,%H:%M"))
        rec_list.append(record.venue.name)
        rec_list.append(record.description)
        writer.writerow(rec_list)
    return response
venue_csv.short_description = "Export Selected Venues to CSV"

def set_manager(modeladmin,request,queryset):
    queryset.update(manager=request.user)

set_manager.short_description = "Manage selected events"
######################################################################

class EventsAdmin(AdminSite):
    site_header = 'MyClub Events Administration'
    site_title = 'MyClub Events Admin'
    index_title = 'MyClub Events Admin Home'
    
admin_site = EventsAdmin(name='eventsadmin')

class AttendeeInline(admin.TabularInline):
    model = Event.attendees.through
    verbose_name = 'Attendee'
    verbose_name_plural = 'Attendees'

class EventInline(admin.TabularInline):
    model = Event
    fields = ('name','event_date')
    extra = 1 # กำหนดว่าจะให้แสดงแท็บกี่อัน

@admin.register(Venue)
@admin.register(Venue,site=admin_site)
class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    # list_display = ('name', 'address', 'phone')
    # list_display_links = ('name', 'address') # ทำให้มีลิงก์คลิกได้ที่ฟิลด์ที่กำหนดในทูเพิล
    # list_display_links = None # None จะทำให้ไม่สามารถคลิกดูได้เลย
    # list_editable = ('phone',) # สามารถอัพเดทข้อมูลได้ทันทีที่หน้าแดชบอร์ด
    # list_editable = list_display # ใส่ value เข้าไปจะทำให้ทุกฟิลด์แก้ไขทันทีได้หมด
    ordering = ('name',)
    search_fields = ('name', 'address')
    # inlines = [
    #     EventInline,
    # ]
    
    def get_list_display(self,request):
        return ('name','address','phone','web')

class EventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Event
        fields = '__all__'

@admin.register(Event)
@admin.register(Event,site=admin_site)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    # fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    actions = [set_manager,venue_csv]
    list_display = ('name', 'event_date', 'venue','manager')
    list_filter = ('event_date', 'venue')
    ordering = ('-event_date',)
    save_as = True # ทำให้บันทึกเรกคอร์ดที่มีอยู่แล้วเป็นเรกคอร์ดใหม่ได้
    inlines = [
        AttendeeInline,
    ]
    fieldsets = (
        ('Required Information', {
            'description': "These fields are required for each event.",
            'fields': (('name', 'venue'), 'event_date')
        }),
        ('Optional Information', {
            'classes': ('collapse',),
            'fields': ('description', 'manager')
        })
    )


# admin.site.register(Venue)
# admin.site.register(Event)
admin_site.register(User)
admin_site.register(Group)
admin.site.register(MyClubUser)
