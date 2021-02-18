from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
import requests
import json

# Create your views here.


def register(request):
    if request.method == 'POST':
        clientkey = request.POST['g-recaptcha-response']
        secretkey = '6Lfz0vgZAAAAAM1H1w4l_d9Elr1-ft8jBmGwtpWW'
        captchaData = {
        'secret': secretkey,
        'response': clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verify = response['success']

        form = UserRegistrationForm(request.POST)
        if form.is_valid() and verify:
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! you can login now.')
            return redirect('login')
        elif not verify:
            messages.warning(request, f'Please validate the CAPTCHA!!!') 
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# def login(request):
#     return render(request, 'users/login.html')