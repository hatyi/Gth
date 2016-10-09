"""
Definition of forms.
"""

from django import forms
from django.utils.translation import ugettext_lazy as _
from app.models import *
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget, Textarea


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
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class PageForm(forms.ModelForm):
    custom_hidden_fields = ['page']
    class Meta:
        model = Page
        fields = ['title', 'description', 
                  #special
                  'page']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class InputGroupForm(forms.ModelForm):
    custom_hidden_fields = ['page', 'page_order']
    class Meta:
        model = ReportInputGroupModel
        fields = ['title', 'description', 
                  #special
                  'page', 'page_order']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class TextInputForm(forms.ModelForm):
    custom_hidden_fields = ['page', 'group', 'page_order', 'group_order', 'input_type']
    class Meta:
        model = TextInputModel
        fields = [
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment',
             
            'default_text', 

            'page', 'group', 'input_type', 'page_order', 'group_order'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }


class SignatureInputForm(forms.ModelForm):
    custom_hidden_fields = ['page', 'group', 'page_order', 'group_order', 'input_type']
    class Meta:
        model = SignatureInputModel
        fields = [
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment', 

            'default_typed_signature', 

            'page', 'group', 'input_type', 'page_order', 'group_order'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }
