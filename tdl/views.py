from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .models import Task
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class ToggleCompleteView(View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.complete = not task.complete
        task.save()
        return redirect('TaskList')

class CustomLoginView(LoginView):
    template_name = 'tdl/login.html'
    fields = 'all'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('TaskList')

class RegisterPage(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'tdl/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('TaskList')
        return render(request, 'tdl/register.html', {'form': form})

class PasswordResetRequestView(View):
    def get(self, request):
        form = PasswordResetForm()
        return render(request, 'tdl/password_reset.html', {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "tdl/password_reset_email.txt"
                    domain = get_current_site(request).domain
                    context = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "username": user.username,
                    }
                    email_content = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email_content, 'your_email@example.com', [user.email], fail_silently=False)
                        messages.success(request, "Password reset email sent successfully!")
                    except Exception as e:
                        messages.error(request, f"Error sending email: {str(e)}")
                        return render(request, 'tdl/password_reset.html', {'form': form})
                return redirect("password_reset_done")
            else:
                messages.error(request, "No user is associated with this email address.")
        return render(request, 'tdl/password_reset.html', {'form': form})

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'tdl/password_reset_confirm.html'
    success_url = reverse_lazy('LogIn')

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Your password has been reset successfully!")
        return super().form_valid(form)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = context['tasks'].filter(user=self.request.user)
        count_incomplete = tasks.filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__icontains=search_input)

        context['tasks'] = tasks
        context['count'] = count_incomplete
        context['search_input'] = search_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tdl/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('TaskList')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('TaskList')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('TaskList')
    template_name = 'tdl/task_delete.html'

