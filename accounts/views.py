from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            return redirect('store:product_list')  # redirect to orders page
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('store:product_list')