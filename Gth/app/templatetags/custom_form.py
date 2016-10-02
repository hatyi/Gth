from django import template
register = template.Library()

@register.inclusion_tag('app/custom_form.html')
def render_custom_form(form_to_render):    
    if not getattr(form_to_render, 'custom_hidden_fields', False):
        return {'fields': [{'field': x, 'hidden': False} for x in form_to_render] }
    return {
        'fields': [
            {
                'field': x, 
                'hidden': x.name in form_to_render.custom_hidden_fields
             } for x in form_to_render
         ] 
    }
    


