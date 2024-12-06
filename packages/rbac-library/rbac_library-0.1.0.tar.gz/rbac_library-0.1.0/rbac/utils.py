from django.contrib.auth.models import Group

def assign_role(user, role_name):
    """Assign a specific role to a user."""
    group, _ = Group.objects.get_or_create(name=role_name)
    user.groups.add(group)

def remove_role(user, role_name):
    """Remove a specific role from a user."""
    group = Group.objects.filter(name=role_name).first()
    if group:
        user.groups.remove(group)
