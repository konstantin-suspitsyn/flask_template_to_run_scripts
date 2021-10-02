# Creates tables if not exists
from hq import db
from hq.user_management.models_user_management import User, Role, UserRoles
from passlib.hash import sha256_crypt


def create_tables() -> None:
    """
    Creating necessary tables
    :return: None
    """
    db.create_all()
    db.session.commit()


def add_user_roles_and_admin() -> None:
    """
    Creates 2 roles and admin user
    :return: None
    """
    # Adding role of authenticated user
    base_role = Role(name='base')
    # Adding role of administrator
    admin_role = Role(name='administrator')
    db.session.add(base_role)
    db.session.add(admin_role)
    db.session.commit()

    # Adding First Administrator
    # Do not forget to change all data
    password = sha256_crypt.hash('admin')

    admin_user = User(email='test@test.com',
                      username='admin',
                      password=password,
                      active=True,
                      first_name='Admin',
                      last_name='Admin',
                      )

    admin_user.roles.append(admin_role)

    db.session.add(admin_user)
    db.session.commit()


if __name__ == '__main__':
    create_tables()
    add_user_roles_and_admin()
