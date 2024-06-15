from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import get_callable, reverse, reverse_lazy
from django.views.generic import View, UpdateView, FormView, CreateView, TemplateView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from core.tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaulttags import csrf_token
from django.contrib.auth import login, authenticate, get_user_model
from django.views.decorators.csrf import csrf_protect
from core.forms import *

User = get_user_model()

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return redirect('home')
    return render(request, 'commons/contact.html')



class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('home')
        else:
            messages.warning(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('home')


class DocumentView(TemplateView):
    template_name = 'commons/home.html'
    model=User
    
    def get_context_data(self, *args, **kwargs):
        context_data= super(DocumentView,self).get_context_data(*args, **kwargs)
        context_data['user_count'] = User.objects.all().count()
        return context_data

class SignUpView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save(False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False  # Deactivate account till it is confirmed

        current_site = get_current_site(self.request)
        mail_subject = 'Activate Account'
        message = render_to_string('emails/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage( mail_subject, message, to=[to_email])
        email.send()
        messages.success(self.request, 'Please Confirm your email to complete registration.')
        user.save()
        return HttpResponseRedirect(reverse('home'))



class UserProfileView(LoginRequiredMixin, UpdateView): #Note that we are using UpdateView and not FormView
    model = User
    form_class = UserProfileForm
    template_name = "registration/profile.html"
    context_object_name = 'user'
    login_url = '/accounts/login/'

    def get_success_url(self, *args, **kwargs):
        return reverse("core:home")

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['form'] = UserProfileForm(instance=self.request.user)
        return context