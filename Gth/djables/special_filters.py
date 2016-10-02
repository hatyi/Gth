from abc import ABC, abstractmethod
from djables.helpers import extract_date_values_from_url

class SpecialFilter(ABC):
    @abstractmethod
    def get_query_expression(self, arg):
        pass

class DjablesText(SpecialFilter):
    def __init__(self, filter, title=''):
        self.filter = filter
        self.title = title

    def get_query_expression(self, arg):
        return self.filter(arg['value'])

class DjablesBetween(SpecialFilter):
    def __init__(self, gt, lt, type='date', title=''):
        self.gt = gt
        self.lt = lt
        self.type = type
        self.title = title

    def get_query_expression(self, arg):
        convert_parameter = lambda value: extract_date_values_from_url(value) if self.type == 'date' else int(value)
        value = convert_parameter(arg['value'])
        if arg['par'] == 'gt':
            return self.gt(value)
        if arg['par'] == 'lt':
            return self.lt(value)
        raise TypeError


class DjablesChoices(SpecialFilter):
    def __init__(self, query_expression, choices, title=''):
        self.query_expression = query_expression
        self.choices = choices
        self.title = title


    def get_query_expression(self, arg):
        index = arg['value']
        return self.query_expression(
            self.choices[index].val)


class DjableChoiceModel():
    @staticmethod
    def create(base_set, val='id', name='name'):
        return {
            str(x.__dict__[val]): 
                DjableChoiceModel(x.__dict__[val],x.__dict__[name]) 
                for x in base_set
        }

    @staticmethod
    def create_for_choices(choices):
        return {
            str(x[0]): DjableChoiceModel(x[0], x[1]) for x in choices
        }

    def __init__(self, val, name):
        self.val = val
        self.name = name