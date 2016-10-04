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
            'report_instance': Report(),
            'report_form': ReportForm(),
            'pages': [
                {
                    'page_number': 1, 
                    'page_instance': Page()
                }
            ]
        }
    return {
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

def get_group_data(group_to_render, id_tag=None):
    if not getattr(group_to_render, 'custom_hidden_fields', False):
        return {'fields': 
                [{
                'field': x, 
                'hidden': False,
                'custom_id': str(id_tag) + '_' + x.name
                } 
            for x in group_to_render] 
        }
    return {
        'fields': [
            {
                'field': x, 
                'hidden': x.name in group_to_render.custom_hidden_fields,
                'custom_id': str(id_tag) + '_' + x.name
             } for x in group_to_render
         ] 
    }

def get_form_data(form_to_render, id_tag=None):
    if not getattr(form_to_render, 'custom_hidden_fields', False):
        return {'fields': 
                [{
                'field': x, 
                'hidden': False,
                'custom_id': str(id_tag) + '_' + x.name
                } 
            for x in form_to_render] 
        }
    return {
        'fields': [
            {
                'field': x, 
                'hidden': x.name in form_to_render.custom_hidden_fields,
                'custom_id': str(id_tag) + '_' + x.name
             } for x in form_to_render
         ] 
    }


def get_page_data(num, page=None):
    if page is None:
        return {
            'page': {
                    'page_form': PageForm(), 
                    'page_instance': Page(), 
                    'page_number': num, 
                    'first_page': num==1, 
                    'original': False, 
                    'inputs': []
             }
         }
    return {
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
                            'page_order': i+1
                        }
                        for i,input_model in enumerate(page.inputs_ordered)
                    ]
        }
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