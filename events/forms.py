from django import forms
from django.forms import Textarea,DateTimeInput
from ckeditor.widgets import CKEditorWidget
from .models import Venue,Event

# formtools

class SurveyForm1(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

class SurveyForm2(forms.Form):
    response1 = forms.CharField(label="What's gerat about our club?",widget=Textarea)
    response2 = forms.CharField(label="What's not so great about our club?",widget=Textarea)

#############################################

class CommitteeForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Event
        fields = ['name','event_date','description']
        widgets = {
            'event_date': DateTimeInput(attrs={'type':'datetime-local'})
        }
        

class MyFormWidget(forms.TextInput):
    class Media:
        css = {
            'all':('events/widget.css',)
        }

class VenueForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Venue
        fields = '__all__'
        widgets = {
            'name':MyFormWidget(attrs={'class':'mywidget'}),
            'address': Textarea(attrs={'cols':40,'rows':3}),
        }
    class Media:
        css = {
            'all':('form.css',)
        }
        js = ('mycustom.js',)
        
    # https://docs.djangoproject.com/en/4.1/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email_address = cleaned_data.get("email_address")
        if not (phone or email_address):
            raise forms.ValidationError(
                "You must enter either a phone number or an email, or both."
            )