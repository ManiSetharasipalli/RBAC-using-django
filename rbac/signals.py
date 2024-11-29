from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_custom_permissions(sender, **kwargs):
    # Get ContentType for User model
    content_type = ContentType.objects.get_for_model(User)

    # Default permissions
    permissions = [
        {'codename': 'can_assign_roles', 'name': 'Can assign roles to users'},
        {'codename': 'can_manage_resources', 'name':'Can manage resources (create, update, delete)'},
        {'codename': 'can_view_users', 'name': 'Can view users'},
        {'codename': 'can_manage_users', 'name': 'Can manage users (create, update, delete)'},
        {'codename': 'can_view_resources', 'name': 'Can view resources'},
        {'codename': 'can_edit_resources', 'name': 'Can edit resources'},
    ]

    # Create permissions
    for perm in permissions:
        Permission.objects.get_or_create(codename=perm['codename'], name=perm['name'], content_type=content_type)

    # Assign permissions to groups
    assign_permissions_to_groups()
 

def assign_permissions_to_groups():
    # Get groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    moderator_group, _ = Group.objects.get_or_create(name='Moderator')
    user_group, _ = Group.objects.get_or_create(name='User')

    # Assign all permissions to Admin
    content_type = ContentType.objects.get_for_model(User)
    all_permissions = Permission.objects.filter(content_type=content_type)
    admin_group.permissions.set(all_permissions)

    # Assign specific permissions to Moderator
    moderator_permissions = Permission.objects.filter(codename__in=[
        'can_view_users', 'can_manage_users', 'can_view_resources', 'can_edit_resources'
    ])
    moderator_group.permissions.set(moderator_permissions)

    # Assign specific permissions to User
    user_permissions = Permission.objects.filter(codename__in=[
        'can_view_resources'
    ])
    user_group.permissions.set(user_permissions)
