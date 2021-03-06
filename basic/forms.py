from django import forms
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class ContactForm(forms.Form):
    firstname = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={"placeholder": "First Name"}))
    lastname = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={"placeholder": "Last Name"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Email"}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={"placeholder": "Subject"}))
    message = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'placeholder': 'Type your message...'}))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['firstname'].label = ""
        self.fields['lastname'].label = ""
        self.fields['email'].label = ""
        self.fields['subject'].label = ""
        self.fields['message'].label = ""

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'gmail.com' not in email:
            raise forms.ValidationError("This is not gmail, bro")
        return email

    def clean_content(self):
        raise forms.ValidationError("Contact form Error!")


class GuestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'gmail.com' not in email:
            raise forms.ValidationError("This is not gmail, bro")
        return email

        class Meta:
            fields = ('email')


class SignInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


# class Registerform(forms.Form):
#     username = forms.CharField()
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(label="Conform Password", widget=forms.PasswordInput)
#
#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Username is Taken!")
#
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Email is Taken!")
#         return email
#
#     def clean(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get('password')
#         password1 = self.cleaned_data.get('password1')
#         if password != password1:
#             raise forms.ValidationError("Password should match, boy")
#         return data

# Registerform again
class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)  # 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False  # send confirmation email
        if commit:
            user.save()
        return user

# 3


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)  # 'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
