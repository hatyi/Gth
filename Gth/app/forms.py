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
        fields = ['bus_id', 'plate_number', 'motor_number', 'bus_image']


class BusServiceForm(forms.ModelForm):
    class Meta:
        model = BusService
        fields = ['bus', 'service_date']
        widgets = {
            'service_date': SelectDateWidget(),
        }



class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = ChoiceModel
        fields = ['name', 'color', 'value', 'is_default_answer', 'is_bad_answer', 'must_comment']




class ReportForm(forms.ModelForm):
    MODAL_TITLE = 'Report'
    custom_hidden_fields = False
    class Meta:
        model = Report
        fields = ['title', 'description', 'needs_bus', 'needs_user_data']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class PageForm(forms.ModelForm):
    MODAL_TITLE = 'Page'
    class Meta:
        model = Page
        fields = ['title', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class InputGroupForm(forms.ModelForm):
    MODAL_TITLE = 'Group'
    class Meta:
        model = ReportInputGroupModel
        fields = ['title', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class TextInputForm(forms.ModelForm):
    MODAL_TITLE = 'Text'
    class Meta:
        model = TextInputModel
        fields = [
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment',
             
            'default_text'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class DateInputForm(forms.ModelForm):
    MODAL_TITLE = 'Date'
    class Meta:
        model = DateInputModel
        fields = [
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment',
             
            'default_date'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class RangeInputForm(forms.ModelForm):
    MODAL_TITLE = 'Range'
    class Meta:
        model = RangeInputModel
        fields = [
            'title', 'description',
            'can_comment', 'must_comment',
             
            'default_value', 'min_value', 'max_value', 'increment'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }

class ChoicesInputForm(forms.ModelForm):
    MODAL_TITLE = 'Choices'
    class Meta:
        model = ChoicesInputModel
        fields = [
            'title', 'description',
            'can_be_empty', 'can_comment', 'must_comment',
             
            'choices'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }


class SignatureInputForm(forms.ModelForm):
    MODAL_TITLE = 'Signature'
    class Meta:
        model = SignatureInputModel
        fields = [
            'title', 'description', 'placeholder', 
            'can_be_empty', 'can_comment', 'must_comment', 

            'default_typed_signature'
        ]
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 5})
            }
