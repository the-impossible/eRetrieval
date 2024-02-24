from django import forms
from e_retrieve_auth.models import *

class AccountCreationForm(forms.ModelForm):

    regNo = forms.CharField(help_text='Enter registration Number', widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-lg input-lg',
            'type': 'text',
            'placeholder': 'Enter Reg Number',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control form-control-lg input-lg',
        }
    ))

    password = forms.CharField(help_text='Enter Password', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control form-control-lg input-lg',
            'type': 'password',
        }
    ))


    def clean_regNo(self):
        regNo = self.cleaned_data.get('regNo')
        if regNo != None:
            if User.objects.filter(username=regNo.upper().strip()).exists():
                raise forms.ValidationError('Registration Number Already taken!')

        return regNo

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise forms.ValidationError("Password should be at least 6 characters!")

        return password


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.username = self.cleaned_data.get('regNo').upper().strip()

        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('regNo', 'name', 'password')

class CreateSingleStudentForm(forms.ModelForm):

    username = forms.CharField(help_text='Enter Registration number', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Registration number',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control',
        }
    ))

    pics = forms.ImageField(required=False, help_text='Select Picture', widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    password = forms.CharField(help_text='Enter Password', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Password',
            'class': 'form-control form-control-lg input-lg',
            'type': 'password',
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username').upper()
        exists = User.objects.filter(username=username).exists()

        if exists:
            raise forms.ValidationError("Account already exist!")

        return username

    class Meta:
        model = User
        fields = ('username', 'name', 'password', 'pics')

class EditCreateSingleStudentForm(forms.ModelForm):

    username = forms.CharField(help_text='Enter Registration number', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Registration number',
        }
    ))

    name = forms.CharField(help_text='Enter Full name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Full name',
            'class': 'form-control',
        }
    ))

    pics = forms.ImageField(required=False, help_text='Select Picture', widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username').upper()
        check = User.objects.filter(username=username)

        if self.instance:
            check = check.exclude(pk=self.instance.pk)

        if check.exists():
            raise forms.ValidationError("Username already exist!")

        return username

    class Meta:
        model = User
        fields = ('username', 'name', 'pics')

class PastQuestionForm(forms.ModelForm):

    course_title = forms.CharField(help_text='Enter Course Title', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter Course Title',
        }
    ))

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="(Select Department)", required=True, help_text="Select department", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label="(Select Semester)", required=True, help_text="Select academic semester", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))


    past_question = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'application/pdf'
        }
    ))


    class Meta:
        model = PastQuestion
        fields = ('course_title', 'session', 'semester', 'department', 'past_question')


class RetrievePastQuestionForm(forms.ModelForm):

    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="(Select Department)", required=True, help_text="Select department", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    session = forms.ModelChoiceField(queryset=Session.objects.all(), empty_label="(Select Session)", required=True, help_text="Select academic session", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), empty_label="(Select Semester)", required=True, help_text="Select academic semester", widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))


    class Meta:
        model = PastQuestion
        fields = ('session', 'semester', 'department')
