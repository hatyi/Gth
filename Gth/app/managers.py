from datetime import datetime
from django.db.models.query_utils import Q
from django.db import models
from itertools import chain
from django.db.models import Min, Avg, Sum





##hard coded Nameless racer id
#nameless_id = 1




#class RacersManager(models.Manager):

#    @staticmethod
#    def nameless_id():
#        return nameless_id


#    def get(self, request, id):
#        if id == nameless_id:
#            return self.nameless()
#        return self.racers(request).get(id = id)


#    def nameless(self):
#        return super(RacersManager, self).get_queryset().get(id = nameless_id)

#    def racers(self, request):
#        return super(RacersManager, self).get_queryset().filter(user=request.user)

#    def without_nameless(self, request):
#        return self.racers(request).exclude(id=nameless_id)

#    def selectable_for_position(self, request, position):
#        user_settings = request.user.settings
#        filter_ids = lambda set: set.exclude(id__in=[x['id'] for x in user_settings.bikesettings_set.exclude(position=position).values('id')])
#        filter_events = lambda set: set if user_settings.event is None or not user_settings.store else set.filter(Q(event__isnull=True) | Q(event=user_settings.event))
#        return compose(filter_events, filter_ids)(self.without_nameless(request))

#    def get_or_create_nameless(self):
#        try:
#            return self.nameless()
#        except:
#            nameless = self.model(id = nameless_id, pk=nameless_id, name='Nameless')
#            nameless.save()
#            return nameless

#    def create_or_update_racer(self, request):
#        strid = request.POST.get('racerId', '')
#        name = request.POST.get('name')
#        phone = request.POST.get('phone')
#        email = request.POST.get('email')
#        birth = datetime.strptime(request.POST.get('birth'), '%Y/%m/%d')
#        gender = request.POST.get('gender') == '1'
#        is_event_member = request.POST.get('eventMember', '') == 'on'

#        if strid != 'None':
#            rid = int(strid)
#            racer = self.racers(request).filter(id=rid).update(
#                name = name,
#                email = email,
#                phone = phone,
#                birthDate = birth,
#                gender = gender)
#        else:
#            racer = self.model(name=name, email=email, phone=phone, birthDate=birth, gender=gender, user=request.user)
#            if is_event_member:
#                racer.event = request.user.settings.event
#            racer.save()

#    def get_racer_for_edit_or_create(self, request):
#        racer_id = request.GET.get('id', None)
#        if racer_id != None:
#            return self.racers(request).get(id=racer_id), True
#        else:
#            return self.model(name='', email=''), False


#class EventsManager(models.Manager):
#    def events_desc(self, request):
#        return self.events(request).order_by('-date')

#    def events(self, request):
#        return super(EventsManager, self).get_queryset().filter(user=request.user)

#    def create_or_update_event(self, request):
#        strid = request.POST.get('eventId')
#        name = request.POST.get('name')
#        place = request.POST.get('place')
#        date = datetime.now()

#        if strid != 'None':
#            eid = int(strid)
#            event = self.events(request).filter(id=eid).update(
#                name = name,
#                place = place)
#            return False, 0
#        else:
#            event = self.model(name=name, place=place, date=date, user=request.user)
#            event.save()
#            return True, event.id

#    def get_event_for_edit_or_create(self, request):
#        event_id = request.GET.get('id', -1)
#        if event_id != -1:
#            return self.events().get(id = int(event_id)), True
#        else:
#            return self.model(name='', place='', date=datetime.now().date()), False

#class DetailsManager(models.Manager):
#    def get_detail(self, request, did = None):
#        if did is not None:
#            detail = request.user.detail_set.get(id=did)
#        else:
#            detail = request.user.detail_set.order_by('-id').first()
#        return detail, detail.sprint_set.all()

#    def create(self, event, user):
#        detail = self.model(event=event, user=user)
#        detail.save()
#        return detail

#class SprintsManager(models.Manager):

#    def sprints(self, request):
#        return super(SprintsManager, self).get_queryset().filter(detail__user=request.user)

    

#    def get_sprints_with(self, request, eid = None, rid = None):

#        order_asc = lambda set: set.order_by('-id')
#        event_filter = lambda set: set.filter(detail__event__id=eid) if eid else set
#        racer_filter = lambda set: set.filter(racer__id=rid) if rid else set

#        return compose(order_asc, racer_filter, event_filter)(self.sprints(request)), eid or rid


#class SettingsManager(models.Manager):

#    def get_sprint_settings_data(self, request):
#        user_settings = request.user.settings

#        create_dict = lambda arrays: dict(bike1=arrays[0], bike2 = arrays[1], 
#                                          bike3 = arrays[2], bike4 = arrays[3])
#        create_array_from_settings = lambda bike_settings: [bike_settings.color, bike_settings.distance, 
#                                                            bike_settings.circumference, bike_settings.active]

#        return create_dict([create_array_from_settings(x) for x in user_settings.bikesettings_set.all()]), user_settings.fps


#    def get_sprint_setup_data(self, request, sprints):
#        user_settings = request.user.settings
#        #user_settings.bikesettings_set.filter(racer=None).update(racer=RacersManager.nameless()) TODO this should be donw some way
#        bike_settings_set = user_settings.bikesettings_set.filter(active=True)


#        format_numbers_in_dict = lambda keys, dict: merge(dict, {k:format_number(dict[k]) for k in keys})

#        check_error = lambda current: merge(current,{'error':'No event'}) if user_settings.store and user_settings.event is None else current
#        add_fps_store = lambda current: merge(current,{'fps':user_settings.fps, 'store': user_settings.store})
#        add_avg_best = lambda current: merge(current, 
#                                             format_numbers_in_dict(['avg', 'best'],
#                                             sprints.filter(detail__event=user_settings.event).aggregate(
#                                                 avg=Avg('finish_time'),best=Min('finish_time')) 
#                                                 if user_settings.event else {'avg':None, 'best':None}))

#        add_racer_count = lambda current: merge(current, {'racer_count': bike_settings_set.count()})
#        create_racer_dict = lambda bike_settings: format_numbers_in_dict(['best', 'overall'],
#                                                    dict(id=bike_settings.racer.id,
#                                                       name=bike_settings.racer.name,
#                                                       position = bike_settings.position,
#                                                       color=bike_settings.color,
#                                                       distance=int(bike_settings.distance/1000),
#                                                       best=sprints.filter(racer=bike_settings.racer).aggregate(
#                                                           best=Min('finish_time'))['best'] if bike_settings.racer.id != nameless_id else None,
#                                                       overall=int(sprints.filter(racer=bike_settings.racer).aggregate(
#                                                           overall=Sum('distance'))['overall']/1000) if bike_settings.racer.id != nameless_id else None
#                                                       ))

#        add_racers = lambda current: merge(current, {'racers': [create_racer_dict(x) for x in bike_settings_set]})
#        return compose(add_racers, add_racer_count, add_avg_best, add_fps_store, check_error)({})


#    def get_settings_ordered(self, request):
#        return request.user.settings.bikesettings_set.order_by('position').all()

   