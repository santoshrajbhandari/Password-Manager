from django import forms
from .models import CustomUser, Credential

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class CredentialForm(forms.ModelForm):
    app_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = Credential
        fields = ['app_name', 'app_username', 'app_password']
        
    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user =user
        raw_password = self.cleaned_data['app_password']
        instance.set_password(raw_password)
        if commit:
            instance.save()
        return instance