from djables.helpers import Singleton
from djables.filter import filter
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf.urls import url


new = 'new'
edit = 'edit'
delete = 'delete'
details = 'details'

def get_instance_names():
    return ('(' + 
        '|'.join(DjablesSingleton.instances)
    + ')')

def get_form_actions():
    return ('(' + 
        '|'.join([new, edit])
    + ')')

def get_special_actions():
    return ('(' + 
        '|'.join([delete, details])
    + ')')

def filter_request(request, model_name):
    result = filter(request, DjablesSingleton.resolve(model_name))
    return JsonResponse(result)

class DjablesSingleton(Singleton):
    instances = {}

    def __init__(self, klass):
        super().__init__(klass)
        DjablesSingleton.instances[klass.url] = klass()

    def __call__(self, *args, **kwds):
        super().__call__(*args, **kwds)
        DjablesSingleton.instances[self.instance.url] = self.instance
        return self.instance

    @staticmethod
    def resolve(model_name):
        return DjablesSingleton.instances[model_name]


@login_required
def table_based_view(request, path):
    model = DjablesSingleton.resolve(path)
    return render(request, 'djables/table_based_page.html', {'model': model})


@login_required
def form_based_view(request, path, djables_method):
    model = DjablesSingleton.resolve(path)
    back_path = '/'  + path

    if not djables_method in model.forms:
        raise Http404()

    forms = get_forms(model, request, djables_method)
    if request.method == 'POST':
        if getattr(model,'save_forms',False):
            if model.save_forms(request, forms):
                return HttpResponseRedirect(back_path)
        elif forms[0].is_valid():
            forms[0].save()
            return HttpResponseRedirect(back_path)
    return render(request, 'djables/form_based_page.html', {'model': model, 'forms': forms, 'back_path':back_path, 'form_title': djables_method + ' ' + model.name})


def get_forms(model, request, djables_method):
    form_type = model.forms[djables_method]
    if getattr(model,'get_forms',False):
        return model.get_forms(request, djables_method)

    id=int(request.GET.get('id', '-1'))
    db_model = get_object_or_404(model.get_base_set(request), id=id) if djables_method == edit and id != -1 else None
    if request.method == 'GET':
        if djables_method == new:
            return [form_type()]
        elif djables_method == edit:
            return [form_type(instance=db_model)]
    if djables_method == new:
        return [form_type(request.POST)]
    elif djables_method == edit:
        return [form_type(request.POST, instance=db_model)]
    raise Http404()


def get_urls():
    return [
        url(r'^' + get_instance_names() + '$', table_based_view),
        url(r'^' + get_instance_names() + '/' + get_form_actions() + '$', form_based_view),
        url(r'^djables_filter/(\w+)$', filter_request),
        url(r'^djables_filter/(\w+\/\w+)$', filter_request),
    ]