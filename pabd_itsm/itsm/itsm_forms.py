# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput
from django.views.generic import FormView
from itsm.models import ITSM_User, Service_request, Work_journal, Asset, ITSM_User
from django.contrib.auth import authenticate

# class editPersonForm(forms.ModelForm):
#     name = forms.CharField(label='Imię:', max_length=30)
#     surname = forms.CharField(label='Nazwisko:', max_length=30)
#     address = forms.CharField(label='Adres:', max_length=60)
#     email_address = forms.CharField(label='E-mail:', max_length=30)
#     gender = forms.CharField(label='Płeć:', max_length=1)
#     login = forms.CharField(label='Login:', max_length=61)
#     creation_date = forms.DateTimeField()
#     last_change_date = forms.DateTimeField()
#     user_type = forms.CharField(label='Rodzaj użytkownika:', max_length=20)
#     user_type = forms.CharField(label='Rodzaj użytkownika:', max_length=12)
#     job_title = forms.CharField(label='Stanowisko:', max_length=40)

class editUserForm(ModelForm):
    class Meta:
        model = ITSM_User
        fields = ['name', 'surname', 'address', 'email_address',
                    'gender', 'login', 'user_type', 'business_unit',
                    'job_title']


class editServiceRequestForm(ModelForm):
    class Meta:
        model = Service_request
        fields = ['title','description','status_id','author_id',
                    'owner_id','resume_date','classification',
                    'business_unit','priority', 'asset_id']
        widgets = {'status_id': TextInput(attrs={'readonly': 'readonly'})}

class createServiceRequestForm(ModelForm):
    class Meta:
        model = Service_request
        fields = ['title','description','classification',
                    'business_unit','priority', 'asset_id']
        widgets = {'status_id': TextInput(attrs={'readonly': 'readonly'})}


class editAssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ['person_id', 'business_unit', 'serial_number', 'title',
                    'code_name', 'status', 'asset_type']
        #widgets = {'status': TextInput(attrs={'disabled': 'disabled'})}


class workJournalForm(ModelForm):
    class Meta:
        model = Work_journal
        fields = ['record_title', 'record_description', 'is_internal']


class UserAuthenticationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = ITSM_User
        fields = ('login', 'password')

    def clean(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']
        if not authenticate(login=login, password=password):
            raise forms.ValidationError("Invalid login")
