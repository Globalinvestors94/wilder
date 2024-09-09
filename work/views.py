from django.shortcuts import render,redirect,get_object_or_404
from .forms import (SignUpForm,UserCreationForm,LoginForm, AgricForm, 
                    BusinessForm, AssestForm,BeginnerForm,DepositForm, 
                    WithdrawForm,PromoForm,FinaleForm,EmailForm,AdminEmail)
from .models import (Referal,AgricGrant,BusinessGrant,AssestGrant,
    InvestBeginner,Deposit,Withdrawal,InvestPromo,InvestFinale)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
import random
from .decorators import allowed_users, admin_only
from django.contrib.auth.models import Group
from datetime import datetime
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
User=get_user_model()


def Home(request,*args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        referal=UserReferal.objects.get(code=code)
        request.session['ref_profile']= referal.id 
        print('id', referal.id)
    except:
        pass
    print(request.session.get_expiry_age())

    form = EmailForm(request.POST)
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        phone = form.cleaned_data.get("phone")
        message = form.cleaned_data.get("message")
        subject = 'Wilder Grants & Investment'
        from_email = settings.EMAIL_HOST_USER
        to_email = [settings.EMAIL_HOST_USER]
        

        context = {"first_name":first_name,"last_name":last_name,"phone":phone, "message":message}
        convert = render_to_string('folder/home_email.html', context)
        convert_txt = render_to_string('folder/home_email.txt', context)

        msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
        msg.attach_alternative(convert, "text/html")
        msg.send()

        messages.info(request, "This means alot to us, we'll get back to you shortly")
        return redirect("work:home")

    return render(request, "folder/home.html", {"form":form})


def AboutUs(request):
    return render(request, "folder/about.html")

@login_required(login_url='/login')
@admin_only
def ChoiceField(request):
    return render(request, "folder/choice.html")


@login_required(login_url='/login')
def Grants(request):
    return render(request, "folder/grant.html")

@login_required(login_url='/login')
def Investment(request):
    return render(request, "folder/investment.html")

@login_required(login_url='/login')
@admin_only
def Profile(request):
    if request.user.is_authenticated:

        dUser = request.user
        rewarded = "Approved"
        depo = Deposit.objects.all().filter(user=dUser, status=rewarded).aggregate(s=Sum('amount'))['s'] or 0

        dUser2 = request.user
        beg = InvestBeginner.objects.all().filter(user=dUser2).aggregate(s=Sum('amount'))['s'] or 0
        pro = InvestPromo.objects.all().filter(user=dUser2).aggregate(s=Sum('amount'))['s'] or 0
        fin = InvestFinale.objects.all().filter(user=dUser2).aggregate(s=Sum('amount'))['s'] or 0
        
        all_invest = beg + pro + fin or 0
        
        act_invest = beg + pro + fin or 0
        

        withdrawal = Withdrawal.objects.all().filter(user=dUser2,status=rewarded).aggregate(s=Sum('amount'))['s'] or 0
        
        withi = Withdrawal.objects.all().filter(user=dUser2)
        
        desit = Deposit.objects.all().filter(user=dUser2)
        
        now = timezone.now()
        four_days_ago = now - timedelta(days=4)
        # print(four_days_ago)


        begin = InvestBeginner.objects.all().filter(user=dUser2)
        beginID = InvestBeginner.objects.filter(user=dUser2, late_updated__gte = four_days_ago,late_updated__lte = now)
        calculate = [instance.beginner_amount() for instance in begin]
        
        promo = InvestPromo.objects.all().filter(user=dUser2)
        promoID = InvestPromo.objects.filter(user=dUser2, late_updated__gte = four_days_ago,late_updated__lte = now)
        calculate2 = [instance.promo_amount() for instance in promo]

        finale = InvestFinale.objects.all().filter(user=dUser2)
        finaleID = InvestFinale.objects.filter(user=dUser2, late_updated__gte = four_days_ago,late_updated__lte = now)
        calculate3 = [instance.finale_amount() for instance in finale]

        add_all = calculate+calculate2+calculate3 

        result = sum(add_all)
        resultM = result-act_invest

        # print(resultM)
        result = resultM

       
        difference2 = depo - act_invest 
        difference = depo - act_invest
        # print(difference)

        after = difference2 + act_invest + result
        
        total_invest = difference 
        # print(total_invest)

        another = total_invest
        total_invest= another


        working = total_invest - withdrawal
        total_invest = working


        if 'depo' in request.POST:
            form = DepositForm(request.POST or None,request.FILES or None, initial={'status':'Pending'})
                
            if form.is_valid():
                user = request.user
                email = request.user.email
                coin = form.cleaned_data.get("coin")
                amount = form.cleaned_data.get("amount")
                status = form.cleaned_data.get("status")
                subject = 'Deposit Confirmation'
                from_email = settings.EMAIL_HOST_USER 
                to_email = [email]
                
                    
                form = form.save(commit=False)
                form.user = request.user

                context = {"user":user,"coin":coin,"amount":amount,"status":status}
                convert = render_to_string('folder/deposit_email.html', context)
                convert_txt = render_to_string('folder/deposit_email.txt', context)

                msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
                msg.attach_alternative(convert, "text/html")
                msg.send()
                form.save()

                context = {"user":user,"coin":coin,"amount":amount,"status":status}
                convert = render_to_string('folder/deposit_email.html', context)
                convert_txt = render_to_string('folder/deposit_email.txt', context)

                msg = EmailMultiAlternatives(subject, convert_txt, from_email, ['kelechinwekes94@gmail.com'])
                msg.attach_alternative(convert, "text/html")
                msg.send()
                form.save()

                form.save()
                messages.success(request, 'Your deposit will be reflected soon.. thanks')
                return redirect('work:profile')

            else:
                form=DepositForm()
        else:
            form=DepositForm()


        if 'withi' in request.POST:
            form = WithdrawForm(request.POST or None,request.FILES or None, initial={'status':'Pending'})
                
            if form.is_valid():
                user = request.user
                email = request.user.email
                address = form.cleaned_data.get("address")
                coin = form.cleaned_data.get("coin")
                amount = form.cleaned_data.get("amount")
                status = form.cleaned_data.get("status")
                from_email = settings.EMAIL_HOST_USER 
                to_email = [email]
                
                    
                form = form.save(commit=False)
                form.user = request.user

                context = {"user":user,"address":address,"coin":coin,"amount":amount,"status":status}
                convert = render_to_string('folder/withdrawal_email.html', context)
                convert_txt = render_to_string('folder/withdrawal_email.txt', context)

                msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
                msg.attach_alternative(convert, "text/html")
                msg.send()

                context = {"user":user,"address":address,"coin":coin,"amount":amount,"status":status}
                convert = render_to_string('folder/withdrawal_email.html', context)
                convert_txt = render_to_string('folder/withdrawal_email.txt', context)
                msg = EmailMultiAlternatives(subject, convert_txt, from_email, ['kelechinwekes94@gmail.com'])
                msg.attach_alternative(convert, "text/html")
                msg.send()

                form.save()
                messages.success(request, 'Your deposit will be reflected soon.. thanks')
                return redirect('work:profile')

            else:
                form=WithdrawForm()
        else:
            form=WithdrawForm()

        withdep = request.user
        witdraw = Withdrawal.objects.all().filter(user=withdep)
        
        dUser4 = request.user
        dep = Deposit.objects.all().filter(user=dUser4)

        profile = Referal.objects.get(user=dUser4)
        my_rec = profile.get_recommended_profiles()

   
    return render(request, "folder/profile.html",
        {"form":form,"depo":depo,"witdraw":witdraw, "dep":dep,"my_rec":my_rec, 
        "profile":profile, "withi":withi,"desit":desit,"begin":begin,"withdrawal":withdrawal,
        "promo":promo,"finale":finale,"result":result,"act_invest":act_invest,
        "total_invest":total_invest,"after":after,"beginID":beginID, 
        "promoID":promoID,"finaleID":finaleID,"resultM":resultM,"all_invest":all_invest})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def AdminControl(request):
    begin = InvestBeginner.objects.all()
    promo = InvestPromo.objects.all()
    finale = InvestFinale.objects.all()
    wit = Withdrawal.objects.all()
    dep = Deposit.objects.all()


    if request.method == 'GET':
        form = AdminEmail()
    else:
        form = AdminEmail(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            message = form.cleaned_data.get("message")
            from_email = settings.EMAIL_HOST_USER
            email = form.cleaned_data.get("email")
            to_email = [settings.EMAIL_HOST_USER]
            subject = "Wilder Grants & Investment"


            context = {"name":name,"message":message}
            convert = render_to_string('folder/client_email.html', context)
            convert_txt = render_to_string('folder/client_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
            msg.attach_alternative(convert, "text/html")
            msg.send()
            messages.info(request, "message sent")
            return redirect("work:ogacontrol")
    context = {"begin":begin, "promo":promo, "finale":finale, "wit":wit, "dep":dep,"form":form} 
    return render(request, "folder/admin.html", context)

@login_required(login_url='/login')
def AgricLoan(request):
    agric = AgricGrant.objects.all()
    if request.method == "POST":
        form = AgricForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            message = form.cleaned_data['message']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            from_email = settings.EMAIL_HOST_USER 
            to_email = [email]
            subject = 'Agricultural Grant Notification'
            
            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()


            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)
            msg = EmailMultiAlternatives(subject, convert_txt, from_email, ['kelechinwekes94@gmail.com'])
            msg.attach_alternative(convert, "text/html")
            msg.send()


            form.save()
            return redirect('work:agric')
            messages.info(request, "You will be notified by email if your grant was approved.")
           
    else:
        form = AgricForm()
        
    context = {"form":form, 'agric':agric}
    return render(request, "folder/agric_loan.html",context)


@login_required(login_url='/login')
def BusinessLoan(request):
    bis = BusinessGrant.objects.all()
    if request.method == "POST":
        form = BusinessForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            message = form.cleaned_data['message']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            from_email = settings.EMAIL_HOST_USER 
            to_email = [email]
            subject = 'Business Grant Notification'
            
            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()


            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)
            msg = EmailMultiAlternatives(subject, convert_txt, from_email, ['kelechinwekes94@gmail.com'])
            msg.attach_alternative(convert, "text/html")
            msg.send()

            form.save()
            return redirect('work:business')
            messages.info(request, "You will be notified by email if your grant was approved.")
           
    else:
        form = BusinessForm()
        
    context = {"form":form, 'bis':bis}
    return render(request, "folder/business_loan.html", context)

@login_required(login_url='/login')
def AssestLoan(request):
    assest = AssestGrant.objects.all()
    if request.method == "POST":
        form = AssestForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            message = form.cleaned_data['message']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            from_email = settings.EMAIL_HOST_USER 
            to_email = [email]
            subject = 'Housing/Assest Notification'
            
            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()


            context = {"user":user,"amount":amount,"message":message,"status":status}
            convert = render_to_string('folder/loan_email.html', context)
            convert_txt = render_to_string('folder/loan_email.txt', context)
            msg = EmailMultiAlternatives(subject, convert_txt, from_email, ['kelechinwekes94@gmail.com'])
            msg.attach_alternative(convert, "text/html")
            msg.send()

            form.save()
            return redirect('work:business')
            messages.info(request, "You will be notified by email if your grant was approved.")
           
    else:
        form = AssestForm()
        
    context = {"form":form, 'assest':assest}
    return render(request, "folder/assest_loan.html", context)

#end for grants


# Investment begin
@login_required(login_url='/login')
def BeginnerInvest(request):
    begin = InvestBeginner.objects.all()
    
    if request.method == "POST":
        form = BeginnerForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            subject="Beginner Investment Plan"
            to_email = [email]
            from_email = settings.EMAIL_HOST_USER


            form = form.save(commit=False)
            form.user = request.user

            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
            msg.attach_alternative(convert, "text/html")
            msg.send()


            try:
                send_mail(
                    subject="Beginner Invest Alert",
                    message = "Please check your dashboard as the boss, to know whose the potential investor", 
                    from_email = settings.EMAIL_HOST_USER, 
                    recipient_list=['kelechinwekes94@gmail.com'], fail_silently=False)
            except  BadHeaderError:
                print("probably no network")

            form.save()
            return redirect('work:profile')
            messages.info(request, "You have sucessfully choosen the beginner plan.")
        else:
            messages.error(request, "error was encountered")    
    else:
        form = BeginnerForm()
        
    context = {"form":form, 'begin':begin}
    return render(request, "folder/begin.html", context)
    

@login_required(login_url='/login')
def PromoInvest(request):
    prom = InvestPromo.objects.all()
    
    if request.method == "POST":
        form = PromoForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            subject="Promo Investment Plan"
            to_email = [email]
            from_email = settings.EMAIL_HOST_USER


            form = form.save(commit=False)
            form.user = request.user

            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
            msg.attach_alternative(convert, "text/html")
            msg.send()


            try:
                send_mail(
                    subject="Promo Invest Alert",
                    message = "Please check your dashboard as the boss, to know whose the potential investor", 
                    from_email = settings.EMAIL_HOST_USER, 
                    recipient_list=['kelechinwekes94@gmail.com'], fail_silently=False)
            except  BadHeaderError:
                print("probably no network")

            form.save()
            return redirect('work:profile')
            messages.info(request, "You have sucessfully choosen the beginner plan.")
        else:
            messages.error(request, "error was encountered")    
    else:
        form = PromoForm()
        
    context = {"form":form, 'prom':prom}
    return render(request, "folder/promo.html", context)



@login_required(login_url='/login')
def FinaleInvest(request):
    fin = InvestFinale.objects.all()
    
    if request.method == "POST":
        form = FinaleForm(request.POST, initial={'status':'Pending'})

        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = request.user
            email = request.user.email
            status = form.cleaned_data['status']
            subject="Finale Investment Plan"
            to_email = [email]
            from_email = settings.EMAIL_HOST_USER


            form = form.save(commit=False)
            form.user = request.user

            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
            msg.attach_alternative(convert, "text/html")
            msg.send()


            try:
                send_mail(
                    subject="Finale Invest Alert",
                    message = "Please check your dashboard as the boss, to know whose the potential investor", 
                    from_email = settings.EMAIL_HOST_USER, 
                    recipient_list=['kelechinwekes94@gmail.com'], fail_silently=False)
            except  BadHeaderError:
                print("probably no network")

            form.save()
            return redirect('work:profile')
            messages.info(request, "You have sucessfully choosen the beginner plan.")
        else:
            messages.error(request, "error was encountered")    
    else:
        form = FinaleForm()
        
    context = {"form":form, 'fin':fin}
    return render(request, "folder/finale.html", context)




def RegistrationView(request):
    profile_id = request.session.get('ref_profile')
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        group = Group.objects.get(name='client')
        user.groups.add(group)
        if profile_id is not None:
            recommeded_by_profile = Referal.objects.get(id=profile_id)
            instance = form.save()
            # group = Group.objects.get(name='client')
            # instance.groups.add(group)
            registered_user = get_user_model().objects.get(id=instance.id)
            registered_profile = Referal.objects.get(user=registered_user)
            registered_profile.recommeded_by = recommeded_by_profile.user
            print(recommeded_by_profile.user)
            registered_profile.save()


        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')

        context = {"username":username}
        convert = render_to_string('folder/reg_email.html', context)
        convert_txt = render_to_string('folder/reg_email.txt', context)

        msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
        msg.attach_alternative(convert, "text/html")
        msg.send()
        

        user = authenticate(username=username, password=password)
        
        return redirect('work:choice')
        messages.info(request, username + 'Your account was created succesfully')
        
    context = {"form":form}
    return render(request, "folder/register.html", context)


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            form=login (request, user)
            messages.success(request, f"Welcome {username} !!!")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            else:
                return redirect('work:choice')
           
        else:
            messages.success(request, "Wrong username or password.. please try again")
    form = LoginForm()                  
    return render(request, "folder/login.html", {'form':form})

def Logout(request):
    logout(request)
    messages.success(request, "You just logged out, see you soon!!!")
    return redirect('work:home')



@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def BeginnerPanel(request,id):
    begin = InvestBeginner.objects.get(id=id)
    dUser = request.user
    rewarded = "Approved"
    total_invest = Deposit.objects.all().filter(user=dUser, status=rewarded).aggregate(s=Sum('amount'))['s'] or 0

    form = BeginnerForm(request.POST or None, request.FILES or None, instance=begin)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user = begin.user
        email = begin.user.email
        status = form.cleaned_data['status']
        subject="Beginner Investment Plan"
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        
        if amount >= total_invest:
            messages.info(request, "No money in client account to make investment.. an email has been sent to client")
            return redirect('invest:ogacontrol')
            

        else:
            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()
 
       
            form.save()
            messages.info(request, "Client Beginner plan has been updated")
            return redirect('work:ogacontrol')


        form = BeginnerForm()
            

    return render(request, "folder/beginpanel.html", {'form':form,'begin':begin})


@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def PromoPanel(request,id):
    promo = InvestPromo.objects.get(id=id)
    dUser = request.user
    rewarded = "Approved"
    total_invest = Deposit.objects.all().filter(user=dUser, status=rewarded).aggregate(s=Sum('amount'))['s'] or 0

    form = PromoForm(request.POST or None, request.FILES or None, instance=promo)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user = promo.user
        email = promo.user.email
        status = form.cleaned_data['status']
        subject="Promo Investment Plan"
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        
        if amount >= total_invest:
            messages.info(request, "No money in client account to make investment.. an email has been sent to client")
            return redirect('invest:ogacontrol')
            

        else:
            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()
 
       
            form.save()
            messages.info(request, "Client Promo plan has been updated")
            return redirect('work:ogacontrol')


        form = PromoForm()

    return render(request, "folder/promopanel.html", {'form':form,'promo':promo})



@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def FinalePanel(request,id):
    finale = InvestFinale.objects.get(id=id)
    dUser = request.user
    rewarded = "Approved"
    total_invest = Deposit.objects.all().filter(user=dUser, status=rewarded).aggregate(s=Sum('amount'))['s'] or 0

    form = FinaleForm(request.POST or None, request.FILES or None, instance=finale)
    if form.is_valid():
        amount = form.cleaned_data['amount']
        user = finale.user
        email = finale.user.email
        status = form.cleaned_data['status']
        subject="Finale Investment Plan"
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        
        if amount >= total_invest:
            messages.info(request, "No money in client account to make investment.. an email has been sent to client")
            return redirect('invest:ogacontrol')
            

        else:
            context = {"user":user,"amount":amount, "status":status}
            convert = render_to_string('folder/invest_email.html', context)
            convert_txt = render_to_string('folder/invest_email.txt', context)

            msg = EmailMultiAlternatives(subject, convert_txt, from_email, to_email)
            msg.attach_alternative(convert, "text/html")
            msg.send()
 
       
            form.save()
            messages.info(request, "Client Finale plan has been updated")
            return redirect('work:ogacontrol')
        form = FinaleForm()
    return render(request, "folder/promopanel.html", {'form':form,'promo':promo})

            

@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def DepositPanel(request,id):
    dep = Deposit.objects.get(id=id)
    form = DepositForm(request.POST or None, request.FILES or None, instance=dep)
    if form.is_valid():
        user = dep.user
        email = dep.user.email
        coin = form.cleaned_data.get("coin")
        amount = form.cleaned_data.get("amount")
        status = form.cleaned_data.get("status")
        subject="Deposit Notice"
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        
        

        context = {"user":user,"amount":amount, "coin":coin, "status":status}
        convert = render_to_string('folder/back_deposit_email.html', context)
        convert_txt = render_to_string('folder/back_deposit_email.txt', context)

        msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
        msg.attach_alternative(convert, "text/html")
        msg.send()


        form.save()
        messages.info(request, "Client deposit has been sucessfully updated")
        return redirect('work:ogacontrol')
    return render(request, "folder/depositPanel.html", {'form':form,'dep':dep})



@login_required(login_url='/login')
@allowed_users(allowed_roles=['operator'])
def WithdrawalPanel(request,id):
    wit = Withdrawal.objects.get(id=id)
    form = WithdrawForm(request.POST or None, request.FILES or None, instance=wit)
    if form.is_valid():
        user = wit.user
        email = wit.user.email
        address = form.cleaned_data.get("address")
        coin = form.cleaned_data.get("coin")
        amount = form.cleaned_data.get("amount")
        status = form.cleaned_data.get("status")
        subject="Withdrawal Notice"
        to_email = [email]
        from_email = settings.EMAIL_HOST_USER
        
    
        context = {"user":user,"amount":amount,"address":address, "coin":coin, "status":status}
        convert = render_to_string('folder/back_withdrawal_email.html', context)
        convert_txt = render_to_string('folder/back_withdrawal_email.txt', context)

        msg = EmailMultiAlternatives(subject, convert_txt, from_email, [email])
        msg.attach_alternative(convert, "text/html")
        msg.send()

        form.save()
        messages.info(request, "Client withdrawal has been sucessfully updated")
        return redirect('work:ogacontrol')
    return render(request, "folder/withdrawalPan.html", {'form':form,'wit':wit})

    