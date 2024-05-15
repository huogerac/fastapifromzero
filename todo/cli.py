import typer
from rich import print
from rich.prompt import Prompt
from sqlalchemy import select

from todo.settings import Settings
from todo.database import engine, get_session
from todo.models.core import Task
from todo.models.users import User
from todo.services.users_service import add_new_user


main = typer.Typer(name="Todo CLI", add_completion=False)


@main.command()
def shell():
    """create the interactive shell"""
    _vars = {
        "settings": Settings(),
        "engine": engine,
        "session": next(get_session()),
        "select": select,
        "Task": Task,
        "User": User,
    }
    typer.echo(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        start_ipython(argv=["--ipython-dir=/tmp", "--no-banner"], user_ns=_vars)
    except ImportError:
        import code

        code.InteractiveConsole(_vars).interact()


@main.command()
def create_user():
    """create a new user"""
    print("[green]This command will create a new user![/green] :boom:")

    name = Prompt.ask("Enter your name :sunglasses:")
    email = typer.prompt("What's the user email?")
    password = Prompt.ask("Enter a password :key:", password=True)
    password_confirmation = Prompt.ask("Repeat the password :key:", password=True)

    if password != password_confirmation:
        print("[bold red]The password doesnt match![/bold red]")
        raise typer.Exit()

    session = next(get_session())
    new_user = add_new_user(session, email, password, email, name)
    print(new_user)
