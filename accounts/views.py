from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import InterestedStock
from .forms import InterestedStockForm, CustomUserCreationForm
from django.db import IntegrityError


def signup(request):
    if request.user.is_authenticated:
        return redirect('crawlings:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('crawlings:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('crawlings:index')  
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('crawlings:index') 

@login_required
def profile(request, username):
    form = InterestedStockForm()
    user_stocks = InterestedStock.objects.filter(user=request.user)

    if request.method == 'POST':
        form = InterestedStockForm(request.POST)
        if form.is_valid():
            new_stock = form.save(commit=False)
            new_stock.user = request.user
            try:
                new_stock.save()
            except IntegrityError:
                messages.warning(request, '이미 추가된 종목입니다!')
            return redirect('accounts:profile', username=username)

    context = {
        'form': form,
        'user_stocks': user_stocks,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def delete_stock(request, pk):
    stock = InterestedStock.objects.get(pk=pk)
    if stock.user == request.user:
        stock.delete()
    return redirect('accounts:profile', username=request.user.username)