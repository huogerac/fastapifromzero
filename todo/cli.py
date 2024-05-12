import typer
from sqlalchemy import select

from todo.settings import Settings
from todo.database import engine
from todo.models.core import Task


main = typer.Typer(name="Todo CLI", add_completion=False)


@main.command()
def shell():
    """create the interactive shell"""
    _vars = {
        "engine": engine,
        "select": select,
        "Settings": Settings,
        "Task": Task,
    }
    typer.echo(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        start_ipython(argv=["--ipython-dir=/tmp", "--no-banner"], user_ns=_vars)
    except ImportError:
        import code

        code.InteractiveConsole(_vars).interact()
