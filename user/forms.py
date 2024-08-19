from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='E-Posta', max_length=200, help_text='zorunlu')
    username = forms.CharField(label='Kullanıcı Adı', max_length=200, help_text='zorunlu')
    
    first_name = forms.CharField(label='Ad', max_length=30, help_text='adınızı girin')
    last_name = forms.CharField(label='Soyad', max_length=30, help_text='soyadınızı girin')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanımda.")
        return email


    # def clean_phone(self):
    #     phone_number = self.cleaned_data['phone_number']
    #     if User.objects.filter(phone_number=phone_number).exists():
    #         raise forms.ValidationError("Bu telefon numarası zaten kullanımda.")
    #     return phone_number

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)




from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CustomPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Yeni Şifre",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Bootstrap class for styling
            #'placeholder': 'Yeni Şifre'  # Placeholder text
        })
    )
    new_password2 = forms.CharField(
        label="Yeni Şifre Tekrar",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
           # 'placeholder': 'Yeni Şifre Tekrar'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Yeni şifreler eşleşmiyor.")
        return cleaned_data



from django import forms
from.models import *
class User_Update_Forms(forms.ModelForm):
    class Meta:
        model=Profile
        fields=[
        'biographys',
        'mobile_phone',
        'avatars',
        'social_media_facebook',
        'social_media_twitter',
        'social_media_instagram',
        'social_media_tiktok'        
        ]