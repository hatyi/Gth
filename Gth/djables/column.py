from djables.cell import DjablesActionCell, DjablesSimpleCell
from djables.helpers import getattr_rec
from djables.special_filters import DjablesBetween, DjablesChoices, DjableChoiceModel, DjablesText
from django.db.models.query_utils import Q
from datetime import datetime


class DjableColumn():

    def __init__(self, 
                 column_name, 
                 visible_name = None,
                 choices_tuple = None, 
                 orderable = True, 
                 filterable = True,
                 between_filter = None,
                 choices_filter = None,
                 row_actions=None, 
                 extras_on_cell=None,
                 format_value=None):

        self.column_name = column_name
        self.visible_name = visible_name or column_name
        self.choices_tuple = choices_tuple
        self.orderable = row_actions is None and orderable
        self.filterable = row_actions is None and filterable
        self.row_actions = row_actions
        self.extras_on_cell = extras_on_cell
        self.format_value = format_value
        self.special_filter = None


    def get_cell(self, model):
        if self.row_actions:
            return DjablesActionCell(self.row_actions(model))
        val = self.__format_value(getattr_rec(model, self.column_name))
        if self.choices_tuple is not None:
            val = dict(self.choices_tuple).get(val, val)
        cell = DjablesSimpleCell(value=val)
        if self.extras_on_cell:
            self.extras_on_cell(cell)
        return cell


    def __format_value(self,value):
        if self.format_value:
            return self.format_value(value)
        if value is None:
            return '-'
        if isinstance(value, datetime):
            return value.strftime('%Y/%m/%d')
        return value


    def text_filter(self, title = None, column_name = None):
        self.special_filter = DjablesText(
                lambda x: Q(**{(column_name or self.column_name) + '__icontains':x}), 
                title or self.visible_name)
        return self


    def between_filter(self, type = 'date', title = None, column_name = None):
        self.special_filter = DjablesBetween(
                lambda x: Q(**{(column_name or self.column_name) + '__gte':x}), 
                lambda x: Q(**{(column_name or self.column_name) + '__lte':x}),
                type, title = title or self.visible_name)
        return self


    def choices_filter(self, choice_set, title = None, column_name = None):
        if type(choice_set) is tuple:
            self.special_filter = DjablesChoices(
                lambda x: Q(**{column_name or self.column_name:x}),
                DjableChoiceModel.create_for_choices(choice_set),
                title=title or self.visible_name)
        else:
            self.special_filter = DjablesChoices(
                lambda x: Q(**{(column_name or self.column_name) + '__id':x}),
                DjableChoiceModel.create(choice_set),
                title=title or self.visible_name)
        return self