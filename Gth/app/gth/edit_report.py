from django.http.response import Http404
from djables import djables_manager as manager
from app.forms import ReportForm, PageForm, TextInputForm, InputGroupForm
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from app.models import Report, Page, ReportInputGroupModel, TextInputModel, ReportInputModel



def save_report(data, method):
    pass

def get_report(data, method):
    if method == manager.new:
        return __create_forms_dict()
    if method == manager.edit:
        id = int(data.get('id', '-1'))
        report = get_object_or_404(Report.objects.filter(Q(active=True)), id=id)
        return __create_forms_dict(report)
    raise Http404()


def __create_forms_dict(report_model = None):
    if not report_model:
        return {
            'report_form': ReportForm(),
            'pages': [
                {'page_form': PageForm(), 'page_instance': Page(), 'page_number': 1, 'inputs': []}
            ]
        }
    return {
            'report_form': ReportForm(instance=report_model),
            'pages': [
                {
                    'page_instance': page,
                    'page_form': PageForm(instance=page),
                    'page_number': i + 1, 
                    'inputs': [
                        {
                            'input_instance': input_model,
                            'input_form': __get_input_form(input_model), 
                            'page_order': i+1
                        }
                        for i,input_model in enumerate(page.inputs_ordered)
                        ]}
                for i,page in enumerate(report_model.pages.all())
            ]
        }


def __get_input_form(input_model):
    def __get_simple_form(model):
        return {
            ReportInputModel.TEXT: lambda x: TextInputForm(instance=x)
        }[model.input_type](model)

    if isinstance(input_model, ReportInputGroupModel):
        return {
            'group_instance': input_model,
            'group_form': InputGroupForm(instance=input_model),
            'inputs': [
                {
                    'input_instance': x,
                    'input_form': __get_simple_form(x), 
                    'group_order': i+1
                } 
                for i,x in enumerate(input_model.inputs.all())
                ]
            }
    return __get_simple_form(input_model)

    

#def edit_report_model(request, method):
#    if request.method == "POST":
#        return JsonResponse({'succes':True})

#    forms = get_report_model_forms(request, method)
#    i = 0
#    for x in forms[1]:
#        if i == 0:
#            forms[1].title_field = x
#        elif i == 1:
#            forms[1].desc_field = x
#        i += 1

#    return render(request, 'app/edit_model.html',{
#        'report_form': forms[0],
#        'page_form': forms[1]
#        })

#def report_model_logic(request, method, form):
#    return JsonResponse({'success':True})


#def get_report_model_forms(request, method):
#    
#    if request.method == 'GET':
#        if method == manager.new:
#            return (ReportForm(),PageForm())
#    #    elif djables_method == manager.edit:
#    #        return [UserForm(instance=report.user), ProfileForm(instance=report)]
#    #if djables_method == manager.new:
#    #    return [UserForm(request.POST), ProfileForm(request.POST)]
#    #elif djables_method == manager.edit:
#    #    return [UserForm(request.POST, instance=report.user), ProfileForm(request.POST, instance=report)]
#    raise Http404()