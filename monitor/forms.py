# -*- coding: utf-8 -*-
__author__ = 'YSQ'
from django import forms
from django.forms import Form, ModelForm
from django.forms import fields
from django.forms import widgets

from .models import *


class MonitorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MonitorForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['secret_id'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['host'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['port'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['monitor_type'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['request_type'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = MonitorAccount
        fields = '__all__'
        exclude = ['create_date', 'create_user']
        widgets = {
            "secret_key": widgets.PasswordInput(attrs={"class": "form-control m-input"})
        }


class ContactRuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactRuleForm, self).__init__(*args, **kwargs)
        self.fields['rule_name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['regex_rule'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_group'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['severity'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = ContactRule
        exclude = ['create_time', 'create_user']


class ContactUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactUserForm, self).__init__(*args, **kwargs)
        self.fields['contact_user'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_address'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_group'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_level'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_type'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = ContactUser
        exclude = ['create_time', 'create_user']
        widgets = {
            "contact_rule": widgets.CheckboxSelectMultiple(
                attrs={"class": "form-control m-bootstrap-select m_selectpicker"}
            )
        }


class ContactGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_name'].widget.attrs.update({'class': 'form-control m-input'})
        self.fields['contact_type'].widget.attrs.update({'class': 'form-control m-input'})

    class Meta:
        model = ContactGroup
        exclude = ['create_time']
