from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from cryptography.fernet import Fernet

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        
        email = self.normalize_email(email)
        encryption_key = Fernet.generate_key().decode()
        user = self.model(email=email, encryption_key=encryption_key, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    encryption_key = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    

class Credential(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=100)
    app_username = models.CharField(max_length=100)
    app_password_encrypted = models.TextField()

    def set_password(self, raw_password):
        key = self.user.encryption_key.encode()  # Store securely!
        f = Fernet(key)
        self.app_password_encrypted = f.encrypt(raw_password.encode()).decode()
        print("Encrypting with key:", self.user.encryption_key)



    def get_password(self):
        key = self.user.encryption_key.encode()
        f = Fernet(key)
        return f.decrypt(self.app_password_encrypted.encode()).decode()
    
    def __str__(self):
        return f"{self.app_name} ({self.app_username})"


    