"""
Definition of urls for Gth.
"""

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
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^login$', app.views.user_login),
    url(r'^logout$', app.views.user_logout),
    url(r'^models/(\w+)$', app.views.edit_report_model),
   
   
    url(r'^', include(djables_manager.get_urls())),
    url(r'^admin/', include(admin.site.urls)),
]
