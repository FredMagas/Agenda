from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label='Username')
    confirm_email = forms.EmailField(label='Confirme o endereço de email', max_length=255, required=True)
    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').capitalize()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').capitalize()
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "Os emails estão diferentes.")
        
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "As senhas estão diferentes.")
        
        # Verificar se o username já existe
        if User.objects.filter(username=username).exists():
            self.add_error('username', "Esse nome de usuário já foi usado. Por favor escolha outro.")

        # Verificar se o email já existe
        if User.objects.filter(email=email).exists():
            self.add_error('email', "Esse email já foi registrado, por favor use um diferente!")

        return cleaned_data