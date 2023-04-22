from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from events.models import Event

register = template.Library()

@register.simple_tag
def show_attendees(e):
  # attds = attendee.e.all()
  e = list(Event.events.filter(name=e))[0]
  attd_to_show = []
  for attendee in e.attendees.all():
    attd_to_show.append(str(attendee.user))
  text_to_show = ','.join(attd_to_show)
  return text_to_show

@register.simple_tag
def create_date(date_val):
  return "This content was created on %s"% date_val.strftime('%A %B %d, %Y')

@register.inclusion_tag('events/announcements.html')
def announcements():
  announcements = [
    {
      'date':'6-10-2020',
      'announcement': "Club Registrations Open"
    },
    {
      'date':'6-15-2020',
      'announcement':"Joe Smith Elected New Club President"
    }
  ]
  return {'announcements':announcements}

@register.filter(name='reverse')
@stringfilter
def reverse(value):
  '''
  ใน Python สัญลักษณ์ :: หมายถึงการใช้ slice หรือการเลือกส่วนหนึ่งของ sequence (เช่น string, list, tuple) โดยสามารถกำหนด start index, end index, และ step
  
  - start คือ index ตัวแรกที่ต้องการเลือก (ถ้าไม่ระบุจะเริ่มต้นจากตัวแรก)
  - end คือ index ตัวสุดท้ายที่ต้องการเลือก (ถ้าไม่ระบุจะถือว่าเป็นตัวสุดท้าย)
  - step คือระยะห่างระหว่าง index ที่ต้องการเลือก (ถ้าไม่ระบุจะใช้ค่าเริ่มต้นเป็น 1)
  
  ดังนั้นใน value[::-1] แสดงว่าเรากำหนดให้ step มีค่าเป็น -1 
  ซึ่งหมายความว่าเราต้องการเรียงลำดับ sequence จากตัวสุดท้ายไปยังตัวแรกของ sequence โดยเลือกทุกตัวที่ห่างกันด้วยระยะ 1 ตัว (step=-1) ซึ่งก็คือการสลับลำดับ sequence ให้กลับด้านหลัง
  '''
  return value[::-1]