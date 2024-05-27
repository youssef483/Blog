from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import SignupForm,LoginForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.
def user_register(request):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            if new_user := authenticate(
                request, username=username, password=password
            ):
                login(request, new_user)
                messages.success(request, 'Email Has Been Created Successfully')
                return redirect('home')
    else:
        form = SignupForm()
        
    context= {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

def profile(request,id):
    profile = Profile.objects.get(id=id)
    if request.POST:
        form = ProfileForm(request.POST,request.FILES, instance= profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('profile', profile.id)
    else:
        form = ProfileForm(instance= profile)
    context = {
        'form':form,
        'profile':profile
    }
    return render(request, 'accounts/profile.html', context)


def user_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            messages.success(request, 'You Have Been Logged in Successfully')
            return redirect('home')
    else:
        form = LoginForm()

    context={'form':form}
    return render(request, 'accounts/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')