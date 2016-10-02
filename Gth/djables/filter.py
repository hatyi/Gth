from djables.helpers import compose, paginate_set

def filter(request, model):
    query_text = request.GET.get('query', None)
    column_order = request.GET.get('order', None)
    special_filters = [dict(column=key[2:-4], arg=dict(value=request.GET.get(key), par=key[-2:])) for key in request.GET if '__' in key]

    query_by_text = lambda input_set: input_set.filter(model.get_query_expression(query_text)) if query_text and model.filterable else input_set
    order_by_column = lambda input_set: input_set.order_by(column_order) if column_order else input_set
    filter_by_special = lambda input_set: input_set.filter(model.get_special_query_expression(special_filters)) if special_filters and model.special_filterable else input_set
    
    finalize_set = lambda input_set: paginate_set([y['id'] for y in input_set.values('id')], model.items_per_page)
    get_result = compose(finalize_set, filter_by_special, order_by_column, query_by_text)

    return {'ids': get_result(model.get_base_set(request))}