from email import message as email_message
import token
from django.shortcuts import render,redirect
from LoginApp.models import newuser
from django.http import HttpResponse
from django.core.mail import send_mail
import uuid
from django.conf import settings
# Create your views here.
def homepage(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request,"home.html")

def SignupPage(request):
    if request.method == "POST":
        uname=request.POST['username']
        email=request.POST['Email1']
        if uname in newuser.objects.all() or email in newuser.objects.all():
            return HttpResponse("username or email id is already registered")    
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

def send_forgot_password_mail(Email1,token):
    
    subject= 'your forget Password link'
    email_message = f'Hi. click on the link to reset your password  http://127.0.0.1:8000/changepassword/{token}/'
    email_from =settings.DEFAULT_FROM_EMAIL
    recepient_list=[Email1,]
    send_mail(subject,email_message,email_from,recepient_list)
    return True

def ForgetPassword(request):
    if request.method == 'POST':
        Email1=request.POST.get('Email1')
        if not newuser.objects.filter(Email1=Email1).first():
            email_message.success(request,'Not Email  found with this data')
            return redirect('forgotpassword')
        
        user_obj=newuser.objects.get(Email1=Email1)
        token =str(uuid.uuid4())
        send_forgot_password_mail(user_obj,token)
        email_message.success(request,'An email is sent')
    return render(request,'forgotpassword.html')

def change_password(request,token):
    contex = {}
    # if request.method == 'POST':
        # username = request.POST.get('username')
    profile_obj = newuser.objects.get(forgot_password_token=token)
    print(profile_obj)

    return render(request,'changepassword.html')


