from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render,redirect
from LoginApp.models import newuser
from django.http import HttpResponse
from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib import messages
# Create your views here.
def homepage(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request,"home.html")

def SignupPage(request):
    if request.method == "POST":
        uname=request.POST['username']
        email=request.POST['Email1']
        if newuser.objects.filter(username=uname).exists() or newuser.objects.filter(Email1=email).exists():
           return HttpResponse("Username or email id is already registered")
        pass1=request.POST['Password1']
        pass2=request.POST['Password2']
        if pass1!=pass2:
            return HttpResponse("your password and confirm password are mismatch!!") 
        else:
            my_user=newuser(username=uname,Email1=email,Password1=pass1,Password2=pass2)
            my_user.save()
            return redirect('login')
        # return HttpResponse("User created successfully.")
        # print(uname,email,pass1,pass2)
    # myuser=newuser.objects.all()
    return render(request,"Signup.html")

def LoginPage(request):
    if request.method == "POST":
        username=request.POST['username']
        pass3=request.POST['password']
        # print(username,pass3)
       
        
        for user in newuser.objects.all():
        #     print(user.username,user.Password1)
            if user.username == username and user.Password1 == pass3:
                request.session['username']=username
                return redirect('home')
        return HttpResponse("Usernaname or password is Incorrect !!!")
               
    return render(request,"Login.html")

def Logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')

def is_token_valid(user_obj):
    # Add your logic for token expiry check if applicable
    # For example, if there is an expiration time of 24 hours:
    token_expiry_time = user_obj.token_created_at + timedelta(hours=24)
    return timezone.now() < token_expiry_time

def send_forgot_password_mail(Email1, token):
    subject = 'Your forget Password link'
    email_message = f'Hi. Click on the link to reset your password: http://127.0.0.1:8000/changepassword/{token}/'
    email_from = settings.DEFAULT_FROM_EMAIL
    recepient_list = [Email1]
    send_mail(subject, email_message, email_from, recepient_list)
    return True

def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('Email1')
        user_obj = newuser.objects.filter(Email1=email).first()
        
        if not user_obj:
            messages.error(request, 'No user found with this email address')
            return redirect('forgotpassword')

        # Generate a new UUID for the token
        token = uuid.uuid4()
        user_obj.forgot_password_token = token
        user_obj.token_created_at = timezone.now()
        user_obj.save()

        send_forgot_password_mail(email, token)
        messages.success(request, 'An email is sent')
    
    return render(request, 'forgotpassword.html')

def change_password(request, token):
    try:
        user_obj = newuser.objects.get(forgot_password_token=token)
    except newuser.DoesNotExist:
        return render(request, 'invalid_token.html')  
    
    if not is_token_valid(user_obj):
        return render(request, 'invalid_token.html')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'changepassword.html', {'error_message': 'Passwords do not match'})

        # Update the user's password
        user_obj.Password1 = new_password
        user_obj.Password2 = confirm_password

        # Optionally, clear the forgot_password_token after the password is changed
        user_obj.forgot_password_token = None

        # Save the user object with the updated password
        user_obj.save()

        return redirect('login')

    return render(request, 'changepassword.html')


