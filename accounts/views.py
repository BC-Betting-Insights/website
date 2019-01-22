from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.conf import settings

def register(request):
     if request.method == 'POST':
          #Get form values
          first_name = request.POST['first_name']
          last_name = request.POST['last_name']
          email = request.POST['email']
          date_of_birth = request.POST['date_of_birth']
          password = request.POST['password']
          password2 = request.POST['password2']



          #Check if passwords match
          if password == password2:
               # Check username
                    if User.objects.filter(email = email).exists():
                         messages.error(request, 'That Email is Taken')
                         return redirect('register')
                    else:
                         #Looks Good
                         user = User.objects.create_user(username = email, password = password, email = email, date_of_birth = date_of_birth, first_name = first_name, last_name = last_name)
                         user.save()
                         # Login after register
                         auth.login(request, user)
                         messages.success(request, 'You are now logged in')
                         return redirect('index')
          else: 
               messages.error(request, 'Passwords do not match')
               return redirect('register')
     else:
          return render(request, 'accounts/register.html')
     
def login(request):
     if request.method == 'POST':
          username = request.POST['username']
          username = username.lower()
          password = request.POST['password']

          user= auth.authenticate(username = username, password = password)

          if user is not None:
               auth.login(request, user)
               messages.success(request, 'You are now logged in')
               return redirect('index')
          else:
               messages.error(request, 'Invalid Credentials')
               return redirect('login')
     else:
          return render(request, 'accounts/login.html')
     
def logout(request):
     if request.method == 'POST':
          auth.logout(request)
          messages.success(request, 'You are now logged out')
          return redirect('index')
     
def dashboard(request):
     user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)

     context = {
          'contacts': user_contacts
     }
     return render(request, 'accounts/dashboard.html', context)


def authenticate_yes(request):
     if not request.user.is_authenticated:
          messages.success(request, 'You must be logged in')
          return redirect('login')
