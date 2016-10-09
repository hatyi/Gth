from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from app.models import Profile, Report
from djables import djables_manager as manager
from django.db.models.query_utils import Q
from app.forms import ReportForm, PageForm, TextInputForm
from app.gth.edit_report import save_report, get_report, get_page_data, get_form_data

@login_required
def home(request):
    return render(
        request,
        'app/index.html',
        {
            
        }
    )

def user_login(request):
    redirect_to_next = request.GET.get('next', '/')
    if request.method != "POST":
        return render(request, 'app/login.html', {'redirect_to': redirect_to_next})
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if (user and user.profile and user.is_active and user.profile.role == Profile.ADMIN):
        login(request, user)
        return HttpResponseRedirect(redirect_to_next)
    return render(request, 'app/login.html', {
        'redirect_to': redirect_to_next,
        'error': 'Invalid credentials.',
        'username': username
        })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def edit_report_model(request, method):
    if request.method == "POST":
        success = save_report(request.POST, method)
        exit = request.GET.get('exit', False)
        if exit and success:
            return HttpResponseRedirect('/models')
        #additional logic here for no success with forms
        return JsonResponse({'succes':success})
    data = get_report(request.GET, method)
    return render(request, 'app/edit_model.html', data)

def get_new_page(request, current_page_count):
    data = get_page_data(int(current_page_count)+1)
    return render(request, 'app/report_model/custom_page.html', data)

def get_new_input(request):
    data = get_form_data(TextInputForm())
    return render(request, 'app/report_model/custom_form.html', data)