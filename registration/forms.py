from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

subject = "ぼっち救出コミュニティ登録確認"
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。
身に覚えの無いメールの場合は無視して下さい。
"""

def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "activate/{}/{}/".format(uid, token)


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True): # フォームに入力した情報を本セーブする
        user = super().save(commit=False) # デフォルトでemailはセーブできないのでまずはuserに"username", "password1", "password2"を仮セーブして入れる
        user.email = self.cleaned_data["email"] # emailも被りなどなく正しかったら
        
        # 認証リンククリックするまでログイン不可にする
        user.is_active = False
        
        if commit:
            user.save() # 本セーブする
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            try:
                user.email_user(subject, message) # email_userメソッドでuserにメールをtry(送信)する

            # 例外処理
            except Exception as e:
                user.delete() # エラーが起きた場合、今登録したデータを削除
        return user # このuserはUserオブジェクト

        
def activate_user(uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception: # ユーザーが見つからなかったら
        return False

    if default_token_generator.check_token(user, token): # ユーザーが見つかったら
        user.is_active = True
        user.save()
        return True
    
    return False