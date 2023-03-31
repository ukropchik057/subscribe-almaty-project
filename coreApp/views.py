from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *

def homePage(request):
    categories = Category.objects.all()
    return render(request, "app/home.html", {
        'categories': categories
    })

def aboutPage(request):
    about = AboutPage.objects.all()
    return render(request, "app/about.html", {
        'about': about
    })

def allService(request, slug=None):
    category = None
    categories = Category.objects.all()
    businesses = Business.objects.all().order_by('-postDate')
    if slug:
        category = get_object_or_404(Category, slug=slug)
        businesses = businesses.filter(category=category)
    return render(request, "app/all-service.html", {
        'category': category,
        'categories': categories,
        'businesses': businesses
    })

def serviceDetail(request, slug):
    business = get_object_or_404(Business, slug=slug)
    return render(request, 'app/service-detail.html', {
        'business': business
    })

def allCompanies(request):
    companies = Business.objects.all()
    return render(request, "alternate.html", {
        'companies': companies
    })


def addQuery(request, slug):
    business = get_object_or_404(Business, slug=slug)
    if request.method == "POST":
        form = AddQueryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.info(request, f"Ваша заявка получена! Ожидайте звонок менеджера для подтверждение записи. "
                                   f"Перейдите в профиль чтобы следить за заявкой")
            return redirect('homePage')
    else:
        form = AddQueryForm()

    return render(request, "user/add-query.html", {
        'form': form,
        'business': business
    })

def deleteUserQuery(request, pk):
    userQuery = get_object_or_404(Query, pk=pk)
    if request.method == "POST":
        userQuery.delete()
        userQuery.user = request.user
        messages.info(request, f"Заявка удалена")
        return redirect("userDataAndQueries")
    return render(request, "user/delete-query.html", {
        'userQuery': userQuery
    })


def userDataAndQueries(request):
    user = request.user
    userQueries = Query.objects.filter(user=user).order_by('-postDate')
    userData = UserDataProfile.objects.filter(user=user)
    return render(request, "user/user-data.html", {
        'user': user,
        'userQueries': userQueries,
        'userData': userData
    })

def userDataProfileEdit(request):
    if request.method == "POST":
        form = UserDataProfileForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.business = request.user
            form.save()
            return redirect('userDataAndQueries')
    else:
        form = UserDataProfileForm()

    return render(request, "user/user-profile.html", {
        'form': form
    })


def userDataAndQueryDetail(request, pk):
    userQuery = get_object_or_404(Query, pk=pk)
    if request.method == "POST":
        if userQuery.isActive == True:
            userQuery.isActive = False
            userQuery.save()
            messages.info(request, f"Запись отменена")
            return redirect('userDataAndQueries')
        else:
            userQuery.isActive = True
            userQuery.save()
            messages.info(request, f"Запись восстановлена")
            return redirect('userDataAndQueries')
    return render(request, "user/user-data-query-detail.html", {
        'userQuery': userQuery
    })

def signUp(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("homePage")
        messages.error(request, "Что-то пошло не так :(")
    else:
        form = NewUserForm()
    return render(request, "user/sign-up.html", {
        'form': form
    })

def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Добро пожаловать, {username}!")
                return redirect("homePage")
            else:
                messages.error(request, "Неверный логин или пароль. Попробуйте заново")
        else:
            messages.error(request, "Неверный логин или пароль. Попробуйте заново")
    else:
        form = AuthenticationForm()
    return render(request, "user/login.html", {
        'form': form
    })

def logoutUser(request):
    logout(request)
    messages.info(request, "Вы вышли из системы")
    return redirect("homePage")