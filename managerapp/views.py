from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, CredentialForm
from django.contrib.auth import authenticate, login
from .models import CustomUser, Credential
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        CustomUser.objects.create_user(email=email, password=password)
        return redirect('login')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            form.add_error(None, "Invlaid credentials")
            
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    form = CredentialForm(request.POST or None)
    credentials = Credential.objects.filter(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'edit':
            cred_id = request.POST.get('credential_id')
            credential = get_object_or_404(Credential, id=cred_id, user=request.user)
            credential.app_name = request.POST.get('app_name')
            credential.app_username = request.POST.get('app_username')
            credential.set_password(request.POST.get('app_password'))
            credential.save()
            return redirect('dashboard')
        
        elif action == 'delete':
            cred_id = request.POST.get('credential_id')
            credential = get_object_or_404(Credential, id=cred_id, user=request.user)
            credential.delete()
            return redirect('dashboard')
        
        elif action == 'add':
            if form.is_valid():
                form.save(user=request.user)
                return redirect('dashboard')
            
    for cred in credentials:
        try:
            cred.decrypted_password = cred.get_password()
        except Exception as e:
            cred.decrypted_password = "Error decrypting"
    
    return render(request, 'dashboard.html', {'credentials': credentials,
                                                  'form': form})

def home(request):
    return render(request, 'home.html')


