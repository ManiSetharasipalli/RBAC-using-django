# RBAC Implementation in Django with DRF

## Description

This project implements Role-Based Access Control (RBAC) using Django and Django REST Framework (DRF). The application provides a robust system for user registration, role management, and access control across different API endpoints.

## Roles

1. **Admin**: Full system control
   - Assign roles to users
   - View and edit all resources

2. **Moderator**: Limited management capabilities
   - View and edit resources
   - Manage users (without role assignment)

3. **User**: Basic access
   - View resources only

## Key Endpoints

### User Registration
- **URL**: `/api/register/`
- **Method**: `POST`
- Registers a new user with default `User` role

### Admin Registration
- **URL**: `/api/register/admin/`
- **Method**: `POST`
- Restricted to existing Admins
- Creates new admin users

### Role Assignment
- **URL**: `/api/assign-role/{user_id}/`
- **Method**: `PATCH`
- Allows Admins to change user roles

### Resource Management
- **View Resources**: `/api/my_resources/`
  - **Method**: `GET`
  - Access based on permissions

- **Edit Resources**: `/api/my_resources/{id}/`
  - **Method**: `PUT`
  - Restricted to users with edit permissions

## Setup and Installation

### Prerequisites
- Python
- Django
- Django REST Framework

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/rbac-django.git
cd rbac-django

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database (MySQL example)
# Update settings.py with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Permissions Overview
- **IsAdmin**: Full system access
- **IsModerator**: View and edit resources
- **IsUser**: View resources only

## Testing
1. Register users
2. Assign roles
3. Test resource access based on roles

## Database Configuration
Supports MySQL. Update `DATABASES` in `settings.py` with your credentials.

## License
[Add your license information]

## Contributing
[Add contributing guidelines]