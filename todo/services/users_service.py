from todo.models.users import User
from todo.services.auth_service import get_password_hash
from todo.exceptions import ConflictValueException


def list_users(session) -> list:
    users_list = session.query(User).all()
    return [item.to_dict_json() for item in users_list]


def add_new_user(session, email: str, password: str, username: str = None, name: str = None) -> dict:

    if not username:
        username = email

    user = session.query(User).filter(User.email == email).first()
    if user:
        raise ConflictValueException(f"The email '{email}' is already in use.")

    new_user = User(
        id=None,
        username=username,
        email=email,
        name=name,
        password=get_password_hash(password),
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user.to_dict_json()
