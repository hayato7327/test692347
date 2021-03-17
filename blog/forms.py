from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import AuthenticationForm
from.models import Comment


       #ユーザー情報変更ページ
class UserChangeForm(forms.ModelForm):
 
    # 入力を必須にするために、required=Trueで上書き
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=20, help_text="20文字以下で入力してください。")
 
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get("instance", None)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        

    class Meta:
        model = get_user_model()
        fields = ("username", "email")
        
 
    def clean_email(self):
        email = self.cleaned_data["email"]
 
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定してください。")
 
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        else:
            if self.user.email == email:
                return email
 
            raise ValidationError("このメールアドレスは既に使用されています。別のメールアドレスを指定してください")


       #コメント投稿フォーム
class CommentCreateForm(forms.ModelForm):


    class Meta:
        model = Comment
        
         #excludeに指定するとcomment_form.htmlに項目を非表示にできる
        exclude = ("target", "accessuser")