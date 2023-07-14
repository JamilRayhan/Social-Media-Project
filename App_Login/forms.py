from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from App_Login.models import UserProfile

class CreateNewUser(UserCreationForm):
    email = forms.EmailField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Email'}))
    username = forms.CharField(required=True, label="", widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1= forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
    password2= forms.CharField(required=True, label="", widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class AuthForm(AuthenticationForm):
    username = forms.CharField(
        required=True, 
        label="",
        widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password= forms.CharField(
        required=True, 
        label="",
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    class Meta:
        model= User
        fields= ('username','password')
        
        
class EditProfile(forms.ModelForm):
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 1,  # Adjust the number of rows as needed
            'cols': 35,  # Adjust the number of columns as needed
            'placeholder': 'Write your bio...',
            'class': 'form-control'  # Add any additional CSS classes for styling
        })
    )
    date_of_birth=forms.DateField(required=False,widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model= UserProfile
        exclude = ('user',)
