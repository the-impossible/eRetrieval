from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.urls import reverse_lazy
from e_retrieve_auth.models import *
from e_retrieve_auth.forms import *


PASSWORD = "12345678"


class HomePage(TemplateView):
    template_name = "frontend/landing.html"


class LoginPageView(View):
    def get(self, request):
        return render(request, 'backend/auth/login.html')

    def post(self, request):
        username = request.POST.get('username').upper().strip()
        password = request.POST.get('password').strip()

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(
                        request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')

        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(
            request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AccountCreationForm
    template_name = "backend/auth/register.html"
    success_message = "Registration Successful you can now login"

    def get_success_url(self):
        return reverse("auth:login")

class DashBoard(LoginRequiredMixin, TemplateView):
    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pq"] = PastQuestion.objects.all().count()
        context["students"] = User.objects.filter(is_staff=False, is_superuser=False).count()
        if self.request.user.is_superuser:
            context["dept"] = Department.objects.all().count()
        return context

class ManageStudentView(LoginRequiredMixin, ListView):

    template_name = "backend/admin/manage_student.html"
    form_class = CreateSingleStudentForm

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False).order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form1"] = self.form_class
        return context

    def post(self, request):

        form1 = self.form_class(request.POST, request.FILES)

        if form1.is_valid():
            instance = form1.save(commit=False)
            instance.password = make_password(PASSWORD)
            instance.save()
            messages.success(request, "Student created successfully!")
        else:

            messages.error(request, form1.errors.as_text())
            return render(request, 'backend/admin/manage_student.html',

                            context={
                                'form1': form1,
                                'form2': self.second_form_class,
                                'object_list': self.get_queryset()
                            })

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("auth:manage_student")

class UpdateStudentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "backend/admin/edit_delete_student.html"
    form_class = EditCreateSingleStudentForm
    success_message = 'Updated Successfully!'

    def get_success_url(self):
        return reverse("auth:manage_student")

class DeleteStudentView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_student')

class ManageAdminView(LoginRequiredMixin, ListView):

    template_name = "backend/admin/manage_admin.html"
    form_class = CreateSingleStudentForm

    def get_queryset(self):
        return User.objects.filter(is_staff=True, is_superuser=True).order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form1"] = self.form_class
        return context

    def post(self, request):

        form1 = self.form_class(request.POST, request.FILES)

        if 'single' in request.POST:

            if form1.is_valid():
                instance = form1.save(commit=False)
                instance.is_staff = True
                instance.is_superuser = True
                instance.password = make_password(PASSWORD)
                instance.save()
                messages.success(
                    request, "Administrator created successfully!")
            else:

                messages.error(request, form1.errors.as_text())
                return render(request, 'backend/admin/manage_admin.html',

                              context={
                                  'form1': form1,
                                  'object_list': self.get_queryset()
                              })

            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("auth:manage_admin")

class UpdateAdminView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "backend/admin/edit_delete_admin.html"
    form_class = EditCreateSingleStudentForm
    success_message = 'Updated Successfully!'

    def get_success_url(self):
        return reverse("auth:manage_admin")

class DeleteAdminView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_admin')

class UpdateProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "backend/profile.html"
    form_class = AccountCreationForm
    success_message = 'Updated Successfully!'

    def get_success_url(self):
        return reverse("auth:manage_admin")

class ChangePassword(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        password0 = request.POST.get('password0')
        password = request.POST.get('password1')
        password1 = request.POST.get('password2')

        if (password != password1):
            messages.error(
                request, 'New password and confirm password does not match!')
            return redirect('auth:update_profile', self.kwargs['pk'])

        if (len(password1) < 6):
            messages.error(
                request, 'password too short! should not be less than 6 characters')
            return redirect('auth:update_profile', self.kwargs['pk'])

        user = User.objects.get(pk=self.kwargs['pk'])

        if not user.check_password(password0):
            messages.error(request, 'Old password incorrect!')
            return redirect('auth:update_profile', self.kwargs['pk'])

        user.set_password(password)
        user.save()

        messages.success(
            request, 'Password reset successful, you can now login!!')
        return redirect('auth:login')

class ManagePastQuestionView(LoginRequiredMixin, ListView):

    template_name = "backend/admin/manage_past_question.html"
    form_class = PastQuestionForm

    def get_queryset(self):
        return PastQuestion.objects.all().order_by('-date_uploaded')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form1"] = self.form_class
        return context

    def post(self, request):

        form1 = self.form_class(request.POST, request.FILES)

        if form1.is_valid():
            form1.save()
            messages.success(request, "Past Question has been uploaded successfully!")
        else:
            messages.error(request, form1.errors.as_text())
            return render(request, 'backend/admin/manage_past_question.html',

                context={
                    'form1': form1,
                    'object_list': self.get_queryset()
                })

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("auth:manage_past_question")

class UpdatePastQuestionView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PastQuestion
    template_name = "backend/admin/edit_delete_past_question.html"
    form_class = PastQuestionForm
    success_message = 'Updated Successfully!'

    def get_success_url(self):
        return reverse("auth:manage_past_question")

class DeletePastQuestionView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PastQuestion
    success_message = 'Deleted Successfully!'
    success_url = reverse_lazy('auth:manage_past_question')

class RetrievePastQuestionView(LoginRequiredMixin, View):

    template_name = "backend/student/manage_past_question.html"
    form_class = RetrievePastQuestionForm
    qs = PastQuestion.objects.none().order_by('-date_uploaded')

    def get(self, request):
        return render(request, self.template_name, context={"form1":self.form_class, "object_list":self.qs})

    def post(self, request):

        form1 = self.form_class(request.POST)

        if form1.is_valid():
            department = form1.cleaned_data.get('department')
            semester = form1.cleaned_data.get('semester')
            session = form1.cleaned_data.get('session')

            past_question = PastQuestion.objects.filter(semester=semester, session=session, department=department).order_by('-date_uploaded')

            return render(request, self.template_name, context={"form1":self.form_class, "object_list":past_question})

        else:
            messages.error(request, form1.errors.as_text())
            return render(request, 'backend/student/manage_past_question.html',

                context={
                    'form1': form1,
                    'object_list': self.qs
                })

