from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created! You can now log in.')
            return redirect('accounts:login')
        return render(request, 'accounts/register.html', {'form': form})