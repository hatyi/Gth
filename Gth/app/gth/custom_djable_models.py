from djables.models import FilterableDjableModel, SpecialFilterableDjableModel
from djables import djables_manager as manager
from djables.djables_manager import DjablesSingleton
from djables.column import DjableColumn
from app.models import Profile, Bus, BusService, Report
from django.db.models.query_utils import Q
from app.forms import ProfileForm, UserForm, BusForm, BusServiceForm
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from djables.cell import DjablesSimpleCell


@DjablesSingleton
class UserDjableModel(SpecialFilterableDjableModel):
    name='User'
    url='users'
    extends = 'app/authenticated.html'

    def get_base_set(self,request):
        return Profile.objects.all()

    @property
    def columns(self):
        return [
            DjableColumn('name', visible_name = 'Name'),
            DjableColumn('user__username', visible_name = 'Username'),
            DjableColumn('user__email', visible_name = 'Email'),
            DjableColumn('role', visible_name = 'Role', choices_tuple = Profile.ROLES).choices_filter(Profile.ROLES, column_name='role'),
            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
        ]

    @property
    def forms(self):
        return {
            manager.new: [UserForm, ProfileForm],
            manager.edit: [UserForm, ProfileForm],
            }

    def get_forms(self, request, djables_method):
        id=int(request.GET.get('id', '-1'))
        profile = get_object_or_404(self.get_base_set(request), id=id) if djables_method == manager.edit and id != -1 else None
        if request.method == 'GET':
            if djables_method == manager.new:
                return [UserForm(), ProfileForm()]
            elif djables_method == manager.edit:
                return [UserForm(instance=profile.user), ProfileForm(instance=profile)]
        if djables_method == manager.new:
            return [UserForm(request.POST), ProfileForm(request.POST)]
        elif djables_method == manager.edit:
            return [UserForm(request.POST, instance=profile.user), ProfileForm(request.POST, instance=profile)]
        raise Http404()


    def save_forms(self, request, forms):
        user_form = forms[0]
        profile_form = forms[1]
        if all((user_form.is_valid(), profile_form.is_valid())):
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.name = user.first_name + ' ' + user.last_name
            profile.save()
            return True
        return False

    @property
    def action_buttons(self):
        return [self.new_button()]

@DjablesSingleton
class BusDjableModel(SpecialFilterableDjableModel):
    name='Bus'
    url='buses'
    extends = 'app/authenticated.html'
    
    def get_base_set(self,request):
        return Bus.objects.all()

    @property
    def columns(self):
        return [
            DjableColumn('bus_id', visible_name = 'Identifier'),
            DjableColumn('plate_number', visible_name = 'Plate Number'),
            DjableColumn('motor_number', visible_name = 'Motor Number'),
            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
        ]

    @property
    def forms(self):
        return {
            manager.new: BusForm,
            manager.edit: BusForm,
            }

    @property
    def action_buttons(self):
        return [DjablesSimpleCell('Service Dates', '/buses/services'), self.new_button()]

@DjablesSingleton
class BusServicesDjableModel(SpecialFilterableDjableModel):
    name='Service Date'
    url='buses/services'
    extends = 'app/authenticated.html'
    
    def get_base_set(self,request):
        return BusService.objects.filter(Q(active=True))

    @property
    def columns(self):
        return [
            DjableColumn('bus__bus_id', visible_name = 'Bus Identifier'),
            DjableColumn('service_date', visible_name = 'Date').between_filter(),
            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
        ]

    @property
    def forms(self):
        return {
            manager.new: BusServiceForm,
            manager.edit: BusServiceForm
            }

    @property
    def action_buttons(self):
        return [DjablesSimpleCell('Back To Buses', '/buses'), self.new_button()]


@DjablesSingleton
class ReportModelDjableModel(FilterableDjableModel):
    name='Report Model'
    url='models'
    extends = 'app/authenticated.html'
    
    def get_base_set(self,request):
        return Report.objects.filter(Q(active=True))

    @property
    def columns(self):
        return [
            DjableColumn('title', visible_name = 'Title'),
            DjableColumn('description', visible_name = 'Description'),
            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
        ]

    @property
    def action_buttons(self):
        return [self.new_button()]

#@DjablesSingleton
#class BookRentDjableModel(SpecialFilterableDjableModel):
#    name='rents'
#    extends = 'app/authenticated.html'
    
#    def get_base_set(self,request):
#        return BookRent.objects.all()

#    @property
#    def columns(self):
#        return [
#            DjableColumn('rented_book__title', visible_name = 'Book title'),
#            DjableColumn('renting_child__name', visible_name = 'Child name'),
#            DjableColumn('rent_price', visible_name = 'Price').between_filter(type='int'),
#            DjableColumn('take_off_date', visible_name = 'Renting date').between_filter(),
#            DjableColumn('bring_back_date', visible_name = 'Retrieve date').between_filter(),
#            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
#        ]

#    @property
#    def action_buttons(self):
#        return [self.new_button]


#@DjablesSingleton
#class FactionDjableModel(SpecialFilterableDjableModel):
#    name='factions'
#    extends = 'app/authenticated.html'
    
#    def get_base_set(self,request):
#        return Faction.objects.all()

#    @property
#    def columns(self):
#        return [
#            DjableColumn('name', visible_name = 'Book title'),
#            DjableColumn('start_date', visible_name = 'Start date').between_filter(),
#            DjableColumn('base_price', visible_name = 'Price').between_filter(type='int'),
#            DjableColumn('status__name', visible_name = 'Stauts').choices_filter(FactionStatus.objects.order_by('-id'), column_name='status'),
#            DjableColumn('Actions', row_actions=lambda x: [self.edit_action(x)]), 
#        ]

#    @property
#    def action_buttons(self):
#        return [self.new_button]