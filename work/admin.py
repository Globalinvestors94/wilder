from django.contrib import admin
from .models import (Referal, AgricGrant, BusinessGrant, AssestGrant,
					InvestBeginner,InvestPromo,InvestFinale,Withdrawal,Deposit)


admin.site.register(Referal)
admin.site.register(AgricGrant)
admin.site.register(BusinessGrant)
admin.site.register(AssestGrant)
admin.site.register(InvestBeginner)
admin.site.register(InvestPromo)
admin.site.register(InvestFinale)
admin.site.register(Withdrawal)
admin.site.register(Deposit)

# Register your models here.
