from core.db.connector import sessionify
from core.db.models import Role, User, Token, Group

admin_name = 'admin'
admin_token = '0b202c64e4ba86a0023a5b8a8a3e2a2b31578cc313340813'

test_client_name = 'client'
test_client_token = 'e8738304de22ffdb812fc151c232af3ee5dd12b557f08d1f'

test_group_name = 'admin_client_group'


def get_admin(session):
    return session.query(User).filter(User.name == admin_name).one_or_none()


def get_admin_token(session):
    return session.query(Token).filter(Token.code == admin_token).one_or_none()


def get_test_client(session):
    return session.query(User).filter(User.name == test_client_name).one_or_none()


def get_test_client_token(session):
    return session.query(Token).filter(Token.code == test_client_token).one_or_none()


def get_test_group(session):
    return session.query(Group).filter(Group.name == test_group_name).one_or_none()


@sessionify()
def fill(session):
    fill_roles(session)
    fill_users(session)
    fill_tokens(session)
    fill_groups(session)


def fill_groups(session):
    # add group
    group = get_test_group(session)
    users = [get_admin(session), get_test_client(session)]
    if not group:
        users = [get_admin(session), get_test_client(session)]
        group = Group(name=test_group_name, users=users)
        session.add(group)
        session.commit()
    else:
        group.users = users
        session.commit()



def fill_users(session):
    # add admin user
    admin = get_admin(session)
    if not admin:
        admin = User(name=admin_name, role_id=Role.ADMIN)
        session.add(admin)
        session.commit()
    # add client user
    client = get_test_client(session)
    if not client:
        client = User(name=test_client_name, role_id=Role.CLIENT)
        session.add(client)
        session.commit()


def fill_tokens(session):
    # add admin token
    token = get_admin_token(session)
    if not token:
        token = Token(code=admin_token, user=get_admin(session))
        session.add(token)
        session.commit()
    # add client token
    token = get_test_client_token(session)
    if not token:
        token = Token(code=test_client_token, user=get_test_client(session))
        session.add(token)
        session.commit()


def fill_roles(session):
    # add admin role
    role_admin = (session.query(Role).filter(Role.name == 'admin').one_or_none()
                  or session.query(Role).filter(Role.id == Role.ADMIN).one_or_none())
    if not role_admin:
        role_admin = Role(id=Role.ADMIN, name='admin')
        session.add(role_admin)
    else:
        role_admin.id = Role.ADMIN
        role_admin.name = 'admin'

    # add client role
    role_client = (session.query(Role).filter(Role.name == 'client').one_or_none()
                   or session.query(Role).filter(Role.id == Role.CLIENT).one_or_none())
    if not role_client:
        role_client = Role(id=Role.CLIENT, name='client')
        session.add(role_client)
    else:
        role_client.id = Role.CLIENT
        role_client.name = 'client'
    session.commit()
