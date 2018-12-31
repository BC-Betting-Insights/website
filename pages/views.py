from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail

from matches.models import Match
from leagues.models import League
from contacts.models import Contact

def index(request):
    matches = Match.objects.order_by('-date').filter(is_played = False)[:3]
    leagues = League.objects.order_by('league_name')
    games_played = Match.objects.count()
    context = {
        'matches': matches,
        'games_played': games_played,
        'leagues': leagues
    }
    return render(request, 'pages/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']


        contact = Contact(name = name, email = email, message = message, user_id = user_id)
        contact.save()

        #Send email
        send_mail(
            'Contact Request',
            'There has been a contact request from ' + name + '.Sign into admin panel for more info',
            'camerongj@outlook.com',
            [email, 'camerongj@outlook.com'],
            fail_silently = False
        )

        messages.success(request, 'Your request has been submitted, we will get back to you')

    return render(request, 'pages/contact.html')
