from django import template
register = template.Library()

@register.inclusion_tag('djables/djable.html')
def djable(model, request):
    paged_set = model.get_processed_set(request)
    special_filters = model.special_filters if model.special_filterable else None
    return {'model': model, 'special_filters': special_filters, 'paged_set': paged_set, 'page_count': len(paged_set)}


@register.inclusion_tag('djables/djable_cell.html')
def djable_cell(cell):
    return {'cell': cell}


@register.inclusion_tag('djables/djable_spec_filter.html')
def djable_filter(x):
    return {'filter': x['filter'], 'name': x['name'], 'type': x['filter'].__class__.__name__}

