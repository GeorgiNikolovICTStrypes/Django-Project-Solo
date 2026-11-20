from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .forms import ModifiedUserCreationForm, ModifiedAuthenticationForm, ModifiedPasswordResetForm, ModifiedSetPasswordForm, UserForm
from .forms import ModifiedChangePasswordForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
# Create your views here.

class RegisterView(CreateView):
    """
    Create a simple register view using 
    custom UserCreationFrom
    temlate name is set to a custom html design
    form_class is a Custom ModifiedUserCreationForm located in .forms
    success_url redirects the user to the login_page
    """
    template_name = 'accounts/login_and_register/register.html'
    form_class = ModifiedUserCreationForm
    success_url = reverse_lazy('loginuser')

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class CustomLoginView(LoginView):
    """
    CustomLoginView extending the built in Django LoginView
    The form_class is a modified AuthenticationForm Class
    the template name is a custom templated in 'accounts/login.html'
    """
    form_class = ModifiedAuthenticationForm
    template_name = 'accounts/login_and_register/login.html'
    next_page = reverse_lazy('dashboard')
    redirect_authenticated_user = True

class CustomPasswordResetView(PasswordResetView):
    """
    CustomPasswordResetView extending the built-in Django PasswordResetView
    The form_class is a modified PasswordResetForm Class
    the template name is a custm template in 'acounts/password_change.html'
    """
    form_class = ModifiedPasswordResetForm
    template_name = 'accounts/password_reset/password_reset.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)    

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """
    Class Based View to serve a template that notifies the user that an email has been sent.
    """
    template_name = 'accounts/password_reset/password_reset_done.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Class based view that serves a template with a form that lets the user change their password.
    """
    template_name = 'accounts/password_reset/password_reset_confirm.html'
    form_class = ModifiedSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """
    A class based view that serves a template to show the password reset is complete
    """
    template_name = 'accounts/password_reset/password_reset_complete.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

class ViewProfileView(DetailView):
    """
    Class based view that serves a template that allows a user to get a detailed view of their profile
    """
    model = User
    template_name = 'accounts/profile_operations/view_profile.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.id != kwargs['pk']:
            return HttpResponseForbidden('Not Allowed')
        return super().dispatch(request, *args, **kwargs)

class EditProfileView(UpdateView):
    """
    Class based view that serves a template that allows the user to edit their own profile.
    """
    model = User
    form_class = UserForm
    template_name = 'accounts/profile_operations/edit_profile.html'
    
    def get_success_url(self):
        """
        A function that sets the success link to view_profile/user.id
        Output:
          HttpResponse with url /view_profile/user.id
        """
        return reverse_lazy('view_profile', kwargs = {'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.id != kwargs['pk']:
            return HttpResponseForbidden('Not Allowed')
        return super().dispatch(request, *args, **kwargs)

class ChangePasswordView(PasswordChangeView):
    """
    Class based view that serves a template that allows a user to change their password
    """
    form_class = ModifiedChangePasswordForm
    template_name = 'accounts/password_change/password_change.html'

class ChangePasswordDoneView(PasswordChangeDoneView):
    """
    Class based view that serves a template that shows the user that the password change has been successful
    """
    template_name = 'accounts/password_change/password_change_done.html'

class DeleteProfileView(DeleteView):
    """
    Class based view that serves a template that allows the user to delete their account
    """
    model = User
    template_name = 'accounts/profile_operations/delete_profile.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        """
        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Positional arguments passed through to the parent method
            **kwargs: Keyword arguments passed through to the parent method
        Overrides the base dispatch method by adding the extra functionality
        of redirecting users to the log in page if they are not authenticated.
        Output:
          (HTTPResponse): Either redirects the user to the login page or returns the Dashboard Page
        """
        if request.user.id != kwargs['pk']:
            return HttpResponseForbidden('Not Allowed')
        return super().dispatch(request, *args, **kwargs)