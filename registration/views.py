from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .forms import activate_user
from .forms import SignUpForm
from django.core.mail import send_mail
from django.shortcuts import redirect


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        if user.id: # もしUserオブジェクトにidが入っていたら(会員登録メールを送信できたら)
            return redirect("send_completely") #redirectはURLnameしか指定できない
        else:
            return redirect("login")

       # SignUpViewで仮登録ボタン押した先のページ
class SendCompletelyView(TemplateView):
    template_name = "registration/send_completely.html"

    
       # 認証リンククリックした先の処理
class ActivateView(TemplateView):
    template_name = "registration/activate.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        # 認証トークンを検証して、
        result = activate_user(uidb64, token, request)
        # コンテクストのresultにTrue/Falseの結果を渡します。
        return super().get(request, result=result, **kwargs)