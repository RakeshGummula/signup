from email import message
from django.shortcuts import render,redirect
from LoginApp.models import newuser
from django.http import HttpResponse
# Create your views here.
def homepage(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request,"home.html")

def SignupPage(request):
    if request.method == "POST":
        uname=request.POST['username']
        email=request.POST['Email1']
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
            if user.username == username and user.Password1 == pass3:
                request.session['username']=username
                return redirect('home')
            else:
                return HttpResponse("Usernaname or password is Incorrect !!!")
               
    return render(request,"Login.html")

def Logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')