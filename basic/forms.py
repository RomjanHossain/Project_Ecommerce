from django import forms


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
