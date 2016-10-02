from abc import ABC, abstractmethod
from djables.helpers import sum_with, paginate_set
from django.db.models.query_utils import Q
from djables.cell import DjablesSimpleCell
from djables import djables_manager as manager


class BaseDjableModel(ABC):

    #MUST IMPLEMENT
    @property
    def name(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def columns(self):
        raise NotImplementedError

    #OPTIONAL    
    @property
    def action_buttons(self):
        return []

    @property
    def forms(self):
        return {}

    @property
    def items_per_page(self):
        return 15

    @property
    def visible_page_button_count(self):
        return 5

    @property
    def activity_indicator_dark(self):
        return True

    @property
    def extends(self):
        return 'app/index.html'

    


    def new_button(self):
        return DjablesSimpleCell('New ' + self.name, self.__url(manager.new))

    def create_action(self, icon_name, href, tool_tip=None):
        return DjablesSimpleCell(value=icon_name, href=href,tool_tip=tool_tip)

    def edit_action(self,model):
        return DjablesSimpleCell('pencil', self.__url(manager.edit, model), 'Edit')

    def delete_action(self,model):
        return DjablesSimpleCell('times', self.__url(manager.delete, model), 'Delete')

    def details_action(self,model):
        return DjablesSimpleCell('info', self.__url(manager.details, model), 'Details')

    def __url(self, type, model = None):
        if model:
            return '/' + self.url + '/' + type + '?id=' + str(model.id)
        return '/' + self.url + '/' + type

    @abstractmethod
    def get_base_set(self, request):
        pass

    def get_processed_set(self, request):
        return paginate_set(
            [dict(id=row_model.id, cells=
                  [column.get_cell(row_model) for column in self.columns]) 
                    for row_model in self.get_base_set(request)], 
            self.items_per_page)

    

class FilterableDjableModel(BaseDjableModel):
    @property
    def filterable(self):
        return True

    @property
    def special_filterable(self):
        return False

    def get_query_expression(self, query_string):
        return sum_with([
                Q(**{x.column_name + '__icontains':query_string}) 
                for x in self.columns if x.filterable
             ], lambda x,y:x|y)


class SpecialFilterableDjableModel(FilterableDjableModel):

    special_filterable = True
    @property
    def special_filters(self):
        return [dict(filter=x.special_filter, name=x.column_name) for x in self.columns if x.special_filter]

    @property
    def special_filters_dict(self):
        return {x.column_name: x.special_filter for x in self.columns if x.special_filter}

    def get_special_query_expression(self, input_dicts):
        sf_dict = self.special_filters_dict
        queries = [sf_dict[x['column']].get_query_expression(x['arg']) for x in input_dicts]
        result = sum_with(queries, lambda x,y: x&y)
        return result



