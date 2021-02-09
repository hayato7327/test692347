from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.save()
        return user