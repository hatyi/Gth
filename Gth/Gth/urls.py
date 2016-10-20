from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.gth.custom_djable_models

from django.conf.urls import include
from django.contrib import admin
from djables import djables_manager
admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.home, name='home'),
    url(r'^login$', app.views.user_login),
    url(r'^driverlogin$', app.views.user_login),
    url(r'^logout$', app.views.user_logout),
    url(r'^models/get_new_group$', app.views.get_new_group),
    url(r'^models/(\w+)$', app.views.edit_report_model),
    url(r'^models/get_new_page/([0-9])$', app.views.get_new_page),
    url(r'^models/get_new_input/([0-9])$', app.views.get_new_input),
    url(r'^models/validate_form/(\w+)$', app.views.validate_form),
    url(r'^models/choices/([\w-]+)$', app.views.get_choices_for_group),
   
   
    url(r'^', include(djables_manager.get_urls())),
    url(r'^admin/', include(admin.site.urls)),
]
