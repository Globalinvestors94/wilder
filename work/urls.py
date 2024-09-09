from django.urls import path
from .views import (Home, AdminControl, RegistrationView, AgricLoan, 
			BusinessLoan, AssestLoan, Login,ChoiceField,Grants,
			Investment,Logout,BeginnerInvest,Profile,PromoInvest,FinaleInvest,
			BeginnerPanel,PromoPanel,FinalePanel,DepositPanel,WithdrawalPanel,
			AboutUs) 
from django.views.generic import ListView
from django.contrib.auth import views as auth_views
# from . views import *
	

app_name = 'work'
urlpatterns =[ 
path(r'', Home, name='home'),
path(r'user_investment_profile', Profile, name='profile'),
path(r'oga_controller', AdminControl, name='ogacontrol'),
path(r'agricultural_grant', AgricLoan, name='agric'),
path(r'business_grant', BusinessLoan, name='business'),
path(r'assest_grant', AssestLoan, name='assest'),
path(r'register', RegistrationView, name='register'),
path(r'login', Login, name='login'),
path(r'about_us', AboutUs, name='about'),
path(r'make_your_choice', ChoiceField, name='choice'),
path(r'grant', Grants, name='grant'),
path(r'investment', Investment, name='investment'),
path(r'beginner_investment', BeginnerInvest, name='begin'),
path(r'promo_investment', PromoInvest, name='promo'),
path(r'finale_investment', FinaleInvest, name='finale'),
path(r'begin_panel/<int:id>', BeginnerPanel, name='begin_panel'),
path(r'promo_panel/<int:id>', PromoPanel, name='promo_panel'),
path(r'finale_panel/<int:id>', FinalePanel, name='finale_panel'),
path(r'deposit_panel/<int:id>', DepositPanel, name='deposit_panel'),
path(r'withdrawal_panel/<int:id>', WithdrawalPanel, name='withdrawal_panel'),
path(r'logout', Logout, name='logout'),


]