from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from app.models import Profile, Report, ReportInputModel, ReportInputGroupModel, TextInputModel, SignatureInputModel, DateInputModel, RangeInputModel, ChoicesInputModel
from djables import djables_manager as manager
from django.db.models.query_utils import Q
from app.forms import ReportForm, PageForm, TextInputForm, InputGroupForm, SignatureInputForm, DateInputForm, RangeInputForm, ChoicesInputForm
from app.gth.edit_report import save_report, get_report, get_page_data, get_group_data, get_input_data, get_form_data, get_choices_data
from django.template import loader

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

    if (user and user.profile and user.is_active and 
        (user.profile.role == Profile.ADMIN or user.profile.role == Profile.COWORKER)):
        login(request, user)
        return HttpResponseRedirect(redirect_to_next)
    return render(request, 'app/login.html', {
        'redirect_to': redirect_to_next,
        'error': 'Invalid credentials.',
        'username': username
        })

def driver_login(request):
    if request.method != "POST":
        raise Http404()
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username=username, password=password)

    if (user and user.profile and user.is_active and 
        user.profile.role == Profile.DRIVER):
        login(request, user)
        return JsonResponse({'user': user})
    raise Http404()


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required
def edit_report_model(request, method):
    if request.method == "POST":
        if method == manager.new:
            success = save_report(request.POST)
        else:
            success = save_report(request.POST, Report.objects.get(id=request.GET.get('id')))

        return JsonResponse({'succes':success})
    data = get_report(request.GET, method)
    data['input_types'] = [{'name': x[1], 'value': x[0]} for x in ReportInputModel.TYPES]
    return render(request, 'app/edit_model.html', data)

@login_required
def get_new_page(request, current_page_count):
    data = get_page_data(int(current_page_count)+1)
    return render(request, 'app/report_model/custom_page.html', data)

@login_required
def get_new_group(request):
    data = get_group_data(ReportInputGroupModel(), )
    return render(request, 'app/report_model/custom_group.html', data)

@login_required
def get_new_input(request, type):
    model = {
            ReportInputModel.TEXT: lambda: TextInputModel(input_type=ReportInputModel.TEXT),
            ReportInputModel.DATE: lambda: DateInputModel(input_type=ReportInputModel.DATE),
            ReportInputModel.SLIDER: lambda: RangeInputModel(input_type=ReportInputModel.SLIDER),
            ReportInputModel.CHOICES: lambda: ChoicesInputModel(input_type=ReportInputModel.CHOICES),
            ReportInputModel.SIGNATURE: lambda: SignatureInputModel(input_type=ReportInputModel.SIGNATURE),
        }[int(type)]()
    data = get_input_data(model, input_type=int(type))
    return render(request, 'app/report_model/custom_input.html', data)


@login_required
def validate_form(request, title):
    if request.method != "POST":
        return Http404()
    form = {
            ReportForm.MODAL_TITLE: lambda: ReportForm(request.POST),
            PageForm.MODAL_TITLE: lambda: PageForm(request.POST),
            InputGroupForm.MODAL_TITLE: lambda: InputGroupForm(request.POST),
            TextInputForm.MODAL_TITLE: lambda: TextInputForm(request.POST),
            DateInputForm.MODAL_TITLE: lambda: DateInputForm(request.POST),
            RangeInputForm.MODAL_TITLE: lambda: RangeInputForm(request.POST),
            ChoicesInputForm.MODAL_TITLE: lambda: ChoicesInputForm(request.POST),
            SignatureInputForm.MODAL_TITLE: lambda: SignatureInputForm(request.POST),
        }[title]()
    data = get_form_data(form)
    data['with_form'] = True
    data['form_class'] = 'modal-form-body'
    template = loader.get_template('app/report_model/custom_form.html')
    html_response = template.render(data, request)
    return JsonResponse({'html': html_response, 'success': form.is_valid()})

@login_required
def get_choices_for_group(request, name):
    data = get_choices_data(name)
    return render(request, 'app/report_model/choices_table.html', data)
