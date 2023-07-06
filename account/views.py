from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,VerifyCodeForm, LoginForm, VerifyCodeForm2
import random
from utils import send_otp_code
from .models import OtpCode,User
from django.contrib import messages
from datetime import timedelta, datetime
import pytz
from django.contrib.auth import authenticate , login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

utc = pytz.UTC

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})
        pass

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            code_dup_check = OtpCode.objects.filter(phone_number=cd['phone'])
            if code_dup_check.exists():
                code_dup_check.delete()
            random_code = random.randint(1000,9999)
            send_otp_code(cd['phone'],random_code)
            OtpCode.objects.create(phone_number=cd['phone'],code=random_code)
            request.session['user_register_info'] = {
                'phone_number': cd['phone'],
                'email':cd['email'],
                'full_name':cd['full_name'],
                'password':cd['password'],
            }
            messages.success(request,'we sent you a code','success')
            return redirect('account:verify_code')
        return render(request, self.template_name ,{'form':form})



class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'account/verify.html'
    #utc = pytz.UTC

    def get(self,request):
        form = self.form_class
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        code = code_instance.code
        return render(request,self.template_name,{'form':form,'code':code})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        otp_sent_time = code_instance.created2
        otp_expire_time = (otp_sent_time + timedelta(minutes=1)).replace(tzinfo=utc)
        now = datetime.now().replace(tzinfo=utc)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code and otp_expire_time > now :
                User.objects.create_user(user_session['phone_number'],
                                         user_session['email'],
                                         user_session['full_name'],
                                         user_session['password'])
                code_instance.delete()
                messages.success(request,'registration success','success')
                return redirect('home:home')
            else:
                messages.error(request,'Expired or wrong code!','danger')
                return redirect('account:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request,'already logged in')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        form = self.form_class
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['user_name'], password = cd['password'])
            if user:
                code_dup_check = OtpCode.objects.filter(phone_number=cd['user_name'])
                if code_dup_check.exists():
                    code_dup_check.delete()
                random_code = random.randint(1000, 9999)
                send_otp_code(cd['user_name'], random_code)
                OtpCode.objects.create(phone_number=cd['user_name'], code=random_code)
                request.session['user_login_info']= {
                    'username':cd['user_name'],
                    'password':cd['password'],
                }
                return redirect('account:verify_code_login')
            elif User.objects.filter(phone_number=cd['user_name']).exists():
                messages.error(request, 'Wrong Pass', 'warning')
                return redirect('home:home')
            messages.error(request, 'User not found!', 'warning')
            return redirect('home:home')
        messages.error(request, 'invalid form info!')
        return redirect('account:User_Login')



class UserLoginVerifyCodeView(View):
    form_class = VerifyCodeForm2
    template_name = 'account/loginverify.html'
    utc = pytz.UTC

    def get(self,request):
        user_session = request.session['user_login_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['username'])
        code = code_instance.code
        form = self.form_class
        return render(request,self.template_name,{'form':form,'code':code})

    def post(self,request):
        form = self.form_class(request.POST)
        user_session = request.session['user_login_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['username'])
        otp_sent_time = code_instance.created2
        otp_expire_time = (otp_sent_time + timedelta(minutes=1)).replace(tzinfo=utc)
        now = datetime.now().replace(tzinfo=utc)
        user = authenticate(request, phone_number=user_session['username'], password=user_session['password'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code: #and otp_expire_time > now:
                login(request, user)
                messages.success(request, 'welcome!','success')
                code_instance.delete()
                return redirect('home:home')
            else:
                messages.error(request,'Expired or wrong code!','danger')
                return redirect('account:verify_code_login')
        return redirect('home:home')


class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.info(request,'Bye!')
        return redirect('home:home')


