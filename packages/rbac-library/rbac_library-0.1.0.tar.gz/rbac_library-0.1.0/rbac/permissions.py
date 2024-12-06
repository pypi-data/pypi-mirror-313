def check_user_role(user, role):
    """Check if a user has a specific role."""
    return user.groups.filter(name=role).exists()

def is_admin(user):
    """Check if the user is an admin."""
    return check_user_role(user, 'admin')

def is_staff(user):
    """Check if the user is a staff member."""
    return check_user_role(user, 'staff')
