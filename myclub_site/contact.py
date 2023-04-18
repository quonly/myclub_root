from django import forms
from django.shortcuts import render, redirect
from django.core.mail import send_mail, get_connection


class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)


def contact(request):
    submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # assert False
            con = get_connection(
                'django.core.mail.backends.console.EmailBackend')
            send_mail(
                cd['subject'],
                cd['message'],
                # get คือการเข้าถึงข้อมูลในฟิลด์ที่เรียก หากไม่มี value ถัดไปจะเป็นค่า default
                cd.get(
                    'email', 'noreply@example.com'),
                ['siteowner@example.com'],
                connection=con
            )
            return redirect('/contact?submitted=True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True

    context = {
        'form': form,
        'submitted': submitted
    }

    return render(request, 'contact/contact.html', context)
