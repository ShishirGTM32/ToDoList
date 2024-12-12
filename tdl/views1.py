from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.views.generic import View, TemplateView,FormView
from django.contrib import messages

User = get_user_model()

class PasswordResetRequestView(View):
    def get(self, request):
        # Display the password reset form
        password_reset_form = PasswordResetForm()
        return render(request, 'tdl/password_reset.html', {'form': password_reset_form})

    def post(self, request):
        # Handle form submission
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "tdl/password_reset_email.txt"
                    domain = get_current_site(request).domain  # Get dynamic domain
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Website',  # You can also make this dynamic
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "user": user,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'sushilgautam2323@gmail.com', [user.email], fail_silently=False)
                    except Exception as e:
                        return HttpResponse(f'Error sending email: {str(e)}')
                    messages.success(request, 'Password reset email sent successfully.')
                    return redirect("password_reset_done")
            else:
                messages.error(request, 'Email address not recognized.')

        return render(request, 'tdl/password_reset.html', {'form': password_reset_form})


class PasswordResetConfirmView(FormView):
    template_name = 'tdl/password_reset_confirm.html'
    form_class = SetPasswordForm

    def form_valid(self, form):
        uidb64 = self.kwargs['uidb64']
        token = self.kwargs['token']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(self.request, "Your password has been reset!")
            return redirect('login')
        else:
            messages.error(self.request, "The reset link is invalid or expired.")
            return redirect('password_reset')


class PasswordResetCompleteView(TemplateView):
    template_name = 'tdl/password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Password reset complete. You can now log in with your new password.'
        return context
