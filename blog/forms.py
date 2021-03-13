from django import forms
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm


class UserChangeForm(forms.ModelForm):
 
    # 入力を必須にするために、required=Trueで上書き
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
 
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
 
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name",
        )
 
    def clean_email(self):
        email = self.cleaned_data["email"]
 
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください。")
 
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            if self.user.email == email:
                return email
 
            raise ValidationError("このメールアドレスは既に使用されています。別のメールアドレスを指定してください")