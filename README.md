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
- **URL**: `/api/register_admin/`
- **Method**: `POST`
- Creates new admin users

### Role Assignment
- **URL**: `/api/assign_role/{user_id}/`
- **Method**: `PATCH`
- Allows Admins to change user roles

### Manage Resources
- **URL**: `/api/manage_resources/`
- **Method**: `GET`
- Shows confirmation message of eligibility

### Resource Management
- **View Resources**: `/api/my_resources/`
  - **Method**: `GET`
  - Shows confirmation message of eligibility

- **Edit Resources**: `/api/edit_resources/`
  - **Method**: `GET`
  - Shows confirmation message of eligibility

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

# Configure database
python manage.py migrate

# Start development server
python manage.py runserver
```

## Environment Configuration

### Create .env File
Create a `.env` file in the project root with the following content:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

## Permissions Overview
- **IsAdmin**: Full system access
- **IsModerator**: View and edit resources
- **IsUser**: View resources only

## Testing
1. Register users
2. Assign roles
3. Test resource access based on roles

## Documentation References
- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)

## Acknowledgements
Special thanks to the Django and Django REST Framework communities for their exceptional documentation and support.
