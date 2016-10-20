from django import template
from app.gth.edit_report import get_page_data, get_form_data, get_group_data, get_input_data, get_choices_data
from django.forms.widgets import CheckboxInput, Select
register = template.Library()

@register.inclusion_tag('app/report_model/custom_group.html')
def render_custom_group(group_to_render):
    return get_group_data(group_to_render)

@register.inclusion_tag('app/report_model/custom_input.html')
def render_custom_input(input_to_render):    
    return get_input_data(input_to_render)

@register.inclusion_tag('app/report_model/custom_form.html')
def render_custom_form(form_to_render, with_form_class = None, with_attribute = None):    
    data = get_form_data(form_to_render)
    if with_form_class:
        data['with_form'] = True
        data['form_class'] = with_form_class
        data['attr'] = with_attribute
    return data

@register.inclusion_tag('app/report_model/custom_modal_form.html')
def render_custom_modal_form(form_to_render, title, modal_id = None, save_id = None, cancel_id = None):    
    return {
        'form': form_to_render,
        'title': title,
        'modal_id': modal_id,
        'save_id': save_id,
        'cancel_id': cancel_id
        }

@register.inclusion_tag('app/report_model/choices_table.html')
def render_choices_table(name):
    return get_choices_data(name)

@register.inclusion_tag('app/report_model/custom_page.html')
def render_custom_page(num, page=None):    
    return get_page_data(num,page) 

@register.filter(name='is_checkbox')
def is_checkbox(field):
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter(name='is_select')
def is_select(field):
    return field.field.widget.__class__.__name__ == Select().__class__.__name__
