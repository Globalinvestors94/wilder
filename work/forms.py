from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import (AgricGrant, BusinessGrant, AssestGrant, InvestBeginner,
	Deposit, Withdrawal,InvestPromo,InvestFinale)
from django.db import transaction

from django.forms import TextInput



class AgricForm(forms.ModelForm):
    class Meta:
        model = AgricGrant
        fields =["message","amount", "status"]

        def save(self, **kwargs):
        	user = kwargs.pop('user')
        	instance = super(AgricGrant, self).save(**kwargs)
        	instance.user = AgricGrant.objects.get(user=user) 
        	instance.save()
        	return instance

class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessGrant
        fields =["message","amount", "status"]

        def save(self, **kwargs):
        	user = kwargs.pop('user')
        	instance = super(AgricGrant, self).save(**kwargs)
        	instance.user = AgricGrant.objects.get(user=user) 
        	instance.save()
        	return instance



class AssestForm(forms.ModelForm):
    class Meta:
        model = AssestGrant
        fields =["message","amount", "status"]

        def save(self, **kwargs):
        	user = kwargs.pop('user')
        	instance = super(AgricGrant, self).save(**kwargs)
        	instance.user = AgricGrant.objects.get(user=user) 
        	instance.save()
        	return instance


class BeginnerForm(forms.ModelForm):
    class Meta:
        model = InvestBeginner
        fields =["amount", "status"]

        def save(self, **kwargs):
        	user = kwargs.pop('user')
        	instance = super(InvestBeginner, self).save(**kwargs)
        	instance.user = InvestBeginner.objects.get(user=user) 
        	instance.save()
        	return instance

class PromoForm(forms.ModelForm):
    class Meta:
        model = InvestPromo
        fields =["amount", "status"]

        def save(self, **kwargs):
            user = kwargs.pop('user')
            instance = super(InvestPromo, self).save(**kwargs)
            instance.user = InvestPromo.objects.get(user=user) 
            instance.save()
            return instance

class FinaleForm(forms.ModelForm):
    class Meta:
        model = InvestFinale
        fields =["amount", "status"]

        def save(self, **kwargs):
            user = kwargs.pop('user')
            instance = super(InvestFinale, self).save(**kwargs)
            instance.user = InvestFinale.objects.get(user=user) 
            instance.save()
            return instance


class SignUpForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=60)
	last_name = forms.CharField(max_length=60)

	class Meta:
		model = User
		fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
	remember_me = forms.BooleanField(required=False)



class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields =["amount","address","coin", "status"]

        def save(self, **kwargs):
            user = kwargs.pop('user')
            instance = super(Withdrawal, self).save(**kwargs)
            instance.user = Withdrawal.objects.get(user=user) 
            instance.save()
            return instance

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields =["amount","coin", "status"]

        def save(self, **kwargs):
            user = kwargs.pop('user')
            instance = super(Deposit, self).save(**kwargs)
            instance.user = Deposit.objects.get(user=user) 
            instance.save()
            return instance

class EmailForm(forms.Form):
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    phone = forms.CharField(widget=TextInput(attrs={'type':'number'}))
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class AdminEmail(forms.Form):
    name = forms.CharField(max_length=60)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)