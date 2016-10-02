from itertools import groupby
from functools import reduce
import datetime

def try_get_int_from_request(request, name):
    return int_try_parse(request.GET.get(name, None))

def int_try_parse(value):
    try:
        return int(value)
    except ValueError:
        return None
    except TypeError:
        return None

def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def merge(a,b):
    c = a.copy()
    c.update(b)
    return c


def first(iterable, predicate):
    return next(x for x in iterable if predicate(x))

def extract_date_values_from_url(date):
    if date == '':
        return None

    values = date.split('-')
    if len(values) == 3:
        y,m,d = [int(x) for x in date.split('-')]
        return datetime.datetime(year=y,month=m,day=d)
    else:
        y,m,d,h,M = [int(x) for x in date.split('-')]
        return datetime.datetime(year=y,month=m,day=d,hour=h,minute=M)

def paginate_set(base_set, items_per_page):
    return [
        dict(page=page+1, items=[x for i,x in  items_with_indicies]) 
        for page, items_with_indicies in groupby(
            enumerate(base_set), 
            lambda index_item_tuple: index_item_tuple[0]//items_per_page
        )]

def getattr_rec(object, name):
    def __getattr_rec(levels, index, object):
        if index == len(levels)-1:
            return getattr(object, levels[index])
        return __getattr_rec(levels, index+1, getattr(object, levels[index]))

    return __getattr_rec(name.split('__'), 0, object)

def sum_with(list, operator):
    if len(list) == 0:
        raise AttributeError
    result = list[0]
    for x in list[1:]:
        result = operator(result, x)
    return result


class Singleton:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance
        