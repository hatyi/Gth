from django.http.response import Http404
from djables import djables_manager as manager
from app.forms import ReportForm, PageForm, TextInputForm, InputGroupForm, SignatureInputForm, ChoicesInputForm, RangeInputForm, DateInputForm
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from app.models import Report, Page, ReportInputGroupModel, TextInputModel, ReportInputModel



def save_report(data, method):
    pass

def get_report(data, method):
    if method == manager.new:
        result = __create_forms_dict()
        return result
    if method == manager.edit:
        id = int(data.get('id', '-1'))
        report = get_object_or_404(Report.objects.filter(Q(active=True)), id=id)
        result = __create_forms_dict(report)
        return result
    raise Http404()


def __create_forms_dict(report_model = None):
    if not report_model:
        result = {
            'report_instance': Report(),
            'report_form': ReportForm(),
            'pages': [
                {
                    'page_number': 1, 
                    'page_instance': Page()
                }
            ]
        }
        return result
    result = {
            'report_instance': report_model,
            'report_form': ReportForm(instance=report_model),
            'pages': [
                {
                    'page_instance': page,
                    'page_number': i + 1
                }
                for i,page in enumerate(report_model.pages.all())
            ]
        }
    return result

def get_input_data(input, id_tag=None):
    result = {
        'input':{
            'input_instance': input,
            'input_form': __get_input_form(input),
            'page_order': input.page_order,
            'group_order': input.group_order,
            'id_tag':id_tag
        }
    }
    return result

    


def get_group_data(group, id_tag=None):
    result = {
        'group':{
            'group_instance': group,
            'group_form': InputGroupForm(instance=group),
            'page_order': group.page_order,
            'inputs': group.inputs_ordered,
            'id_tag':id_tag
        }
    }
    return result

def get_form_data(form_to_render, id_tag=None):
    if not getattr(form_to_render, 'custom_hidden_fields', False):
        result = {
            'fields': [
                {
                    'field': x, 
                    'hidden': False,
                    'custom_id': str(id_tag) + '_' + x.name
                } 
            for x in form_to_render] 
        }
        return result
    result = {
        'fields': [
            {
                'field': x, 
                'hidden': x.name in form_to_render.custom_hidden_fields,
                'custom_id': str(id_tag) + '_' + x.name
             } for x in form_to_render
            ] 
        }
    return result


def get_page_data(num, page=None):
    if page is None:
        result = {
            'page': {
                    'page_form': PageForm(), 
                    'page_instance': Page(), 
                    'page_number': num, 
                    'first_page': num==1, 
                    'original': False, 
                    'inputs': []
             }
        }
        return result
    result = {
            'page': {
                    'page_form': PageForm(instance=page), 
                    'page_instance': page, 
                    'page_number': num, 
                    'first_page': num == 1, 
                    'original': True, 
                    'inputs': [
                        {
                            'input_instance': input_model,
                            'input_form': __get_input_form(input_model), 
                            'is_group': isinstance(input_model, ReportInputGroupModel),
                            'page_order': i+1
                        }
                        for i,input_model in enumerate(page.inputs_ordered)
                    ]
            }
        }
    return result

    

def __get_input_form(input_model):
    def __get_simple_form(model):
        result = {
            ReportInputModel.TEXT: lambda x: TextInputForm(instance=x),
            ReportInputModel.DATE: lambda x: DateInputForm(instance=x),
            ReportInputModel.RANGE: lambda x: RangeInputForm(instance=x),
            ReportInputModel.CHOICES: lambda x: ChoicesInputForm(instance=x),
            ReportInputModel.SIGNATURE: lambda x: SignatureInputForm(instance=x)
        }[model.input_type](model)
        return result

    if isinstance(input_model, ReportInputGroupModel):
        result = {
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
        return result
    return __get_simple_form(input_model)