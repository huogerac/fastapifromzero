from todo.models.users import User


def list_users(session) -> list:
    users_list = session.query(User).all()
    return [item.to_dict_json() for item in users_list]


def add_new_user(session, email: str, password: str, username: str = None, name: str = None) -> dict:

    if not username:
        username = email

    new_user = User(
        id=None,
        username=username,
        email=email,
        name=name,
        password=password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user.to_dict_json()
