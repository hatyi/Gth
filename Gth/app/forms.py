"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from app.models import *
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_id', 'plate_number', 'motor_number']


class BusServiceForm(forms.ModelForm):
    class Meta:
        model = BusService
        fields = ['bus', 'service_date']
        widgets = {
            'service_date': SelectDateWidget(),
        }







class ReportForm(forms.ModelForm):
    custom_hidden_fields = False
    class Meta:
        model = Report
        fields = ['title', 'description']

class PageForm(forms.ModelForm):
    custom_hidden_fields = ['page']
    class Meta:
        model = Page
        fields = ['title', 'description', 
                  #special
                  'page']

class InputGroupForm(forms.ModelForm):
    class Meta:
        model = ReportInputGroupModel
        fields = ['title', 'description', 
                  #special
                  'page', 'page_order']

class TextInputForm(forms.ModelForm):
    class Meta:
        model = TextInputModel
        fields = [
            'default_text', 
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment', 
            #special
            'page', 'group', 'input_type', 'page_order', 'group_order'
        ]