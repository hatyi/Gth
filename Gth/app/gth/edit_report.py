from django.http.response import Http404
from djables import djables_manager as manager
from app.forms import ReportForm, PageForm, TextInputForm, InputGroupForm, SignatureInputForm, ChoicesInputForm, RangeInputForm, DateInputForm, ChoiceModelForm
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from app.models import Report, Page, ReportInputGroupModel, TextInputModel, ReportInputModel, ChoiceGroup, ChoicesInputModel, DateInputModel, RangeInputModel, SignatureInputModel
from django.db.models.deletion import ProtectedError
import re


def save_report(data, report_obj = None):
    def get_form(prefix):
        if 'input_' in prefix:
            type = {x[1]: x[0] for x in ReportInputModel.TYPES}[prefix.split('_')[-1]]
            result = {
                ReportInputModel.TEXT: lambda: TextInputForm(data, prefix=prefix),
                ReportInputModel.DATE: lambda: DateInputForm(data, prefix=prefix),
                ReportInputModel.SLIDER: lambda: RangeInputForm(data, prefix=prefix),
                ReportInputModel.CHOICES: lambda: ChoicesInputForm(data, prefix=prefix),
                ReportInputModel.SIGNATURE: lambda: SignatureInputForm(data, prefix=prefix)
            }[type]()
            if 'group_' in prefix:
                group_num = int(re.search('group_([0-9]+)', prefix).group(0).split('_')[-1])
                return result, True, group_num
            on_page_num = int(re.search('input_([0-9]+)', prefix).group(0).split('_')[-1])
            return result, False, on_page_num
        if 'group_' in prefix:
            group_num = int(re.search('group_([0-9]+)', prefix).group(0).split('_')[-1])
            return InputGroupForm(data, prefix=prefix), group_num
        if 'page_' in prefix:
            page_num = int(re.search('page_([0-9]+)', prefix).group(0).split('_')[-1])
            return PageForm(data, prefix=prefix), page_num
        return ReportForm(data, prefix=prefix, instance=report_obj)
    prefixes = data['prefixes'].split('|')
    forms = [get_form(x) for x in prefixes]
    print(forms)

    #try:
    #    report_obj.pages.all().delete()
    #    current_report = next(x for x in forms if isinstance(x, ReportForm)).save()
    #except ProtectedError:
    #    report_obj.pk = None
    #    report_obj.id = None

    #    new_report_obj = report_obj.save()
    #    report_obj.active = False
    #    new_report_obj.parent = report_obj()
    #    new_report_obj.save()
    #    current_report = new_report_obj



def get_choices_data(name):
    print(name)
    if not name or name == 'Ok-NotOk-NotApplicable' or name == 'Yes-No-NotApplicable':
        return None
    return {'choices': [
        {y.name: y for y in ChoiceModelForm(instance=x)}
        for x in  ChoiceGroup.objects.get(name=name).choices.all()]}


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

def get_input_data(input, id_tag=None, input_type=None):
    current_input = {
        ReportInputModel.TEXT: lambda: input if isinstance(input, TextInputModel) else input.textinputmodel,
        ReportInputModel.DATE: lambda: input if isinstance(input, DateInputModel) else input.dateinputmodel,
        ReportInputModel.SLIDER: lambda: input if isinstance(input, RangeInputModel) else input.sliderinputmodel,
        ReportInputModel.CHOICES: lambda: input if isinstance(input, ChoicesInputModel) else input.choicesinputmodel,
        ReportInputModel.SIGNATURE: lambda: input if isinstance(input, SignatureInputModel) else input.signatureinputmodel,
        }[input_type or input.input_type]()
    result = {
        'input':{
            'input_instance': current_input,
            'input_form': __get_input_form(current_input),
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
            for x in form_to_render],
            'form' : form_to_render
        }
        return result
    result = {
        'fields': [
            {
                'field': x, 
                'hidden': x.name in form_to_render.custom_hidden_fields,
                'custom_id': str(id_tag) + '_' + x.name
             } for x in form_to_render
            ],
            'form' : form_to_render
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
            ReportInputModel.SLIDER: lambda x: RangeInputForm(instance=x),
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