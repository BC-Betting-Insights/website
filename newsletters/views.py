from django.contrib import messages
from django.shortcuts import render

from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm

def Newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Your email already exists in our database', "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request, 'Your email has been submitted to the database', "alert alert-success alert-dismissible")

    context ={
        'form': form,
    }
    template = "newsletters/sign_up.html"
    return render(request, template, context)

def Newletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been removed from our mailing list', "alert alert-success alert-dismissible")
        else:
            messages.warning(request, 'Your email is not in the database', "alert alert-warning alert-dismissible")


    context ={
        'form': form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)