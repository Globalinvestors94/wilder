from django.db import models
import random
from django.utils import timezone
# import datetime
from datetime import datetime
from django.conf import settings
from .utils import generate_ref_code
from django.contrib.auth.models import User

CHOICES = [
	('Select Coin','Select Coin'),
	('Bitcoin','Bitcoin'),
	('Ethurum','Ethurum'),
	('Litcoin','Litcoin'),
	]

STATUS = [
	('Pending','Pending'),
	('Processing','Processing'),
	('Approved','Approved'),
	]

# Create your models here.

class Referal (models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referrals")
	code = models.CharField(max_length=12, blank=True)
	recommeded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="referred_by")
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username}"

	def get_recommended_profiles(self):
		query = Referal.objects.all()
		my_rec = [ur for ur in query if ur.recommeded_by == self.user]
		return my_rec


	def save(self, *args, **kwargs):
		if self.code == "":
			code = generate_ref_code()
			self.code = code
		super().save(*args, **kwargs)


class AgricGrant(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	message = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	created = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username


class BusinessGrant(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	message = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	created = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username


class AssestGrant(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	message = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	created = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username


class InvestBeginner(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	late_updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username

	def beginner_amount (self):
		return self.amount * 5 /100 + self.amount


class InvestPromo(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	late_updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username

	def promo_amount(self):
		return self.amount * 10 /100 + self.amount


class InvestFinale(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	amount = models.IntegerField()
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	late_updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.user.username

	def finale_amount(self):
		return self.amount * 15 /100 + self.amount


class Withdrawal(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	address = models.CharField(max_length=200)
	coin = models.CharField(max_length=100, choices=CHOICES, default='Select Coin')
	amount = models.IntegerField()
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	def __str__(self):
		return self.user.username


class Deposit(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	coin = models.CharField(max_length=100, choices=CHOICES, default='Select Coin')
	amount = models.IntegerField()
	status = models.CharField(max_length=100, choices=STATUS, default='Pending')
	def __str__(self):
		return self.user.username


