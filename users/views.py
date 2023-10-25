from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import format_html
from .forms import CustomLoginForm, CustomRegisterForm, CustomPasswordChangeForm, CustomPasswordResetForm, UpdateUserForm, UpdateProfileForm
from .models import Profile
from django.db.models.query_utils import Q
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import transaction

# Funkcje/Klasy zwracającek widok w postaci np. templatu
# oraz sterujące danymi, komujnikujące się z bazą danych


# aktywacja konata. wywoływana po kliknęciu w link aktywacyjny
# w wiadomości email otrzymanej po zarejestrowaniu
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Dziękujemy za weryfikację adresu e-mail. Teraz możesz się zalgować")
        return redirect('users:login-view')
    else:
        messages.error(request, "Nieprawidłowy link aktywacyjny!")

    return redirect('users:dashboard-view')

# wysyłanie wiadomości email do nowego użytkownika po rejestracji
# z linkiem aktywacyjnym do konta
def activateEmail(request, user, to_email):
    mail_subject = "Aktywuj swoje konto"
    message = render_to_string("registration/activate_account_message.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, format_html("Zarejestrowano urzytkownikia <strong>{user_name}</strong>. Sprawdź e-mail: <b>{email}</b> i kliknij w link w wiadomości w celu aktywacji konta. <b>Uwaga:</b> Sprawdź folder ze spamem.", user_name=user, email=to_email))
    else:
        messages.error(request, format_html("Wystąpił problem z wysłaniem wiadomości na e-mail: {email}, sprawdź czy jest poprawny.", email=to_email))

# formularz logowania do strony widok pustego + obsługa
# przesłanego
@user_passes_test(lambda user: not user.is_authenticated, login_url='users:dashboard-view', redirect_field_name=None)
def login_view(request):
    try:
        next_page = request.GET['next']
    except:
        next_page = "/users/dashboard"
    if request.user.is_authenticated:
        return HttpResponseRedirect(next_page)
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                messages.error(request, ("Nazwa użytkownika lub hasło są nieprawidłowe! Spróbuj ponownie."))
                return redirect('login')
        else:
            LoginForm = CustomLoginForm()
            return render(request, 'registration/login.html', {'form': LoginForm})
        
# wylogowywanie użytkownika 
def logout_view(request):
    if request.user.is_authenticated:
        messages.success(request, ("Pomyślnie wylogowano."))
    logout(request)
    return redirect('login')

# formularz rejestracji do strony widok pustego + obsługa
# przesłanego
@user_passes_test(lambda user: not user.is_authenticated, login_url='users:dashboard-view', redirect_field_name=None)
def register_view(request):
    if request.method == "POST":
        RegisterForm = CustomRegisterForm(request.POST)
        if RegisterForm.is_valid():
            user = RegisterForm.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, RegisterForm.cleaned_data.get('email'))
            return redirect('login')
        else:
            messages.warning(request, ("Błąd w formularzu."))
    else:
        RegisterForm = CustomRegisterForm()
    return render(request, "registration/register.html", {'form': RegisterForm})

# widok profilu: zrealizowane quizy, obecna liczba punktów,
# ustawienia konta
@login_required(login_url='users:login-view')
def dashboard_view(request):
    about_user = Profile.objects.get(user=request.user).about_me
    return render(request, 'registration/dashboard.html',{'userName': request.user.first_name, 'aboutUser': about_user})

# zmiana hasła użytkownika widok pustego + obsługa
# przesłanego
@login_required(login_url='users:login-view')    
def password_change_view(request):
    user = request.user
    if request.method == 'POST':
        PasswordChangeForm = CustomPasswordChangeForm(user, request.POST)
        if PasswordChangeForm.is_valid():
            PasswordChangeForm.save()
            user = authenticate(request, username=user.username, password=request.POST['new_password1'])
            login(request, user)
            messages.success(request, ("Hasło zostało zmienione"))
            return redirect('users:dashboard-view')
        else:
            messages.warning(request, ("Błąd w formularzu."))
    PasswordChangeForm = CustomPasswordChangeForm(user)
    return render(request, 'registration/password_change.html', {'form': PasswordChangeForm})

# formularz wysyłania wiadomości email z linkiem resetującym hasło
# widok pustego + obsługa przesłanego. 
@user_passes_test(lambda user: not user.is_authenticated, login_url='users:login-view', redirect_field_name=None)    
def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Reset hasła"
                message = render_to_string("registration/reset_password_message.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, format_html("Wysłano wiadomość z linkiem resetującym hasło"))
                else:
                    messages.error(request, "Błąd wysyłania wiadomości")

            return redirect('users:login-view')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "Musisz przejść test ReCaptcha")
                continue

    form = CustomPasswordResetForm()
    return render(request, "registration/password_reset.html", {"form": form})

# resetowanie hasła z linku w wiadomości email
def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordChangeForm(user, request.POST)
            if form.is_valid():
                user.is_active = True
                form.save()
                messages.success(request, "Twoje hasło zostało zmienione. Teraz możesz się zalogować.")
                return redirect('users:login-view')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = CustomPasswordChangeForm(user)
        return render(request, 'registration/password_reset.html', {'form': form})
    else:
        messages.error(request, "Link wygasł.")

    messages.error(request, 'Błąd. Przekierowanie...')
    return redirect("users:login-view")

# formularz edycji danych osobowych w profilu użytkownika
# widok pustego + obsługa przesłanego 
@login_required
@transaction.atomic
def profile_edit(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Dane zostały zmienione.')
            return redirect('users:dashboard-view')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'registration/user_update.html', {'user_form': user_form, 'profile_form': profile_form})
