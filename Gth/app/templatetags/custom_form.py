from django import template
from app.gth.edit_report import get_page_data, get_form_data, get_group_data, get_input_data
register = template.Library()

@register.inclusion_tag('app/report_model/custom_group.html')
def render_custom_group(group_to_render, page, id_tag = None):
    return get_group_data(group_to_render, page, id_tag)

@register.inclusion_tag('app/report_model/custom_input.html')
def render_custom_input(input_to_render, page, id_tag = None):    
    return get_input_data(input_to_render, page, id_tag)

@register.inclusion_tag('app/report_model/custom_form.html')
def render_custom_form(form_to_render, id_tag = None):    
    return get_form_data(form_to_render, id_tag)


@register.inclusion_tag('app/report_model/custom_page.html')
def render_custom_page(num, page=None):    
    return get_page_data(num,page) 
