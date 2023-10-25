from django import forms
from django.contrib.auth.models import User
from .models import Profile
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, SetPasswordForm, PasswordResetForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox, ReCaptchaV3

# poniżej znajdują się klasy na podstawie, których generowane są 
# przez widoki formularze i umieszczane do odpowiedniego templatu

# w klasach określono typy, nazwy pól wybranych na podstawie modelu

# w niektrzch polach zmieniono dmyślne nazwy oraz tekst pomocniczy,
# ponieważ model User jest dostarczany razem z django i zawiera już
# te informacje ale w języku angielskim

class CustomLoginForm(AuthenticationForm):
    username = UsernameField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'autofocus': True}),
        error_messages={
                'required': "Podaj nazwę użytkownika.",
                'invalid': "Błędne hasło lub nazwa użytkownika.",
            },
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'id': 'pass_name'}),
        error_messages={
                'required': "Podaj hasło.",
                'invalid': "Błędne hasło lub nazwa użytkownika.",
            },
    )

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    first_name = forms.CharField(
        label="Imie",
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )
    last_name = forms.CharField(
        label="Nazwisko",
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control'}),
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = "Nazwa użytkownika"
        self.fields['username'].help_text = ""

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = "Hasło"
        self.fields['password1'].help_text = "<ul><li>Hasło nie może być podobne do podanych wyżej informcji.</li><li>Hasło musi zawierać min. 8 znaków.</li><li>Hasło nie może być powszechnie używanym hasłem.</li><li>Hasło nie może składać się wyłącznie z cyfr.</li></ul>"

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = "Powtórz hasło"
        self.fields['password2'].help_text = "Wprowadź to samo hasło, co poprzednio, w celu weryfikacji."

        self.fields['captcha'].label = ""

    def save(self, commit=True):
        user = super(CustomRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
    
class CustomPasswordChangeForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1' 'new_password2']

    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].label = "Nowe hasło"
        self.fields['new_password1'].help_text = "<ul><li>Hasło nie może być podobne do podanych wyżej informcji.</li><li>Hasło musi zawierać min. 8 znaków.</li><li>Hasło nie może być powszechnie używanym hasłem.</li><li>Hasło nie może składać się wyłącznie z cyfr.</li></ul>"

        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].label = "Powtórz hasło"
        self.fields['new_password2'].help_text = "Wprowadź to samo hasło, co poprzednio, w celu weryfikacji."

class CustomPasswordResetForm(PasswordResetForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

        self.fields['captcha'].label = ""

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nazwa użytkownika",
        )
    first_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Imię",
        )
    last_name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nazwisko",
        )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class UpdateProfileForm(forms.ModelForm):
    about_me = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={"rows": "4", "maxlength": "600"}),
        label="O mnie",
        )
    brith_date = forms.DateField(
        required=False, 
        widget=DatePickerInput(),
        label="Data Urodzenia",
        )
    
    class Meta:
        model = Profile
        fields = ('brith_date', 'about_me')
