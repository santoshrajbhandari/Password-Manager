# SecureVault — Password Manager
SecureVault is a secure, multi-user password manager built with Django. It uses per-user encryption keys to store credentials safely, integrates Gmail OAuth2 for authentication, and frontend with modal dialogs, confirmation flows, and responsive design.

## Key Features
- **Secure Credential**: Storage Passwords are encrypted using Fernet symmetric encryption with per-user keys.
- **Per-User Encryption Keys**: Each user has a unique key stored securely, isolating their data from others.

- **Gmail OAuth2 Login**: Authenticate using Google accounts for seamless access.

- **Session Management**: Includes session expiration logic for added security.

- **Admin Registration**: Backend access for managing users.

- **Responsive UI**: Modal dialogs for editing/deleting credentials, confirmation prompts, and mobile-friendly design.

## Installation
### Clone the repo
```bash
# clone the repository
git clone https://github.com/santoshrajbhandari/Password-Manager.git
cd PasswordManager
```
### Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
### Install dependencies
```bash
pip install -r requirements.txt

```
### Set environment variables 
Create a .env file:
```bash
SECRET_KEY=your-django-secret-key
```
### Run migrations
```bash
python manage.py makemigrations
python manage.py migrate

```
### Start the server
```bash
python manage.py runserver
```
## Credential Encryption
Each credential is encrypted using the user’s key:
```python
def set_password(self, raw_password):
    key = self.user.encryption_key.encode()
    f = Fernet(key)
    self.app_password_encrypted = f.encrypt(raw_password.encode()).decode()

```
