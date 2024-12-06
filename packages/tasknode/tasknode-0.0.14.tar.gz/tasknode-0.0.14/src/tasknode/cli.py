import typer

import tasknode.auth as auth
import tasknode.tasks as tasks

app = typer.Typer(no_args_is_help=True)


def show_available_commands(ctx: typer.Context, value: bool = True):
    if value:
        # fmt: off
        typer.echo("\n📋 Available Commands\n")

        typer.echo("🔑 Account Management:")
        typer.echo("  • signup                   Sign up for a TaskNode account")
        typer.echo("  • login                    Log in to your TaskNode account")
        typer.echo("  • logout                   Log out of your TaskNode account")
        typer.echo("  • resend-verification      Resend the email verification code")
        typer.echo("  • reset-password           Reset your account password")
        typer.echo("  • whoami                   Show current user information")

        typer.echo("\n🚀 Task Management:")
        typer.echo("  • submit                   Submit a Python script to run")
        typer.echo("  • list-jobs                List your TaskNode jobs")

        typer.echo("\nℹ️  Help:")
        typer.echo("  • help                     Show help for the TaskNode CLI")

        typer.echo("")  # Add a newline
        # fmt: on
        raise typer.Exit()


@app.callback()
def callback(
    ctx: typer.Context,
    help: bool = typer.Option(None, "--help", "-h", is_eager=True, callback=show_available_commands),
):
    """
    TaskNode CLI - Run your Python scripts in the cloud
    """
    pass


@app.command()
def help():
    """
    Show help for the TaskNode CLI.
    """
    show_available_commands(None, True)


@app.command()
def login(
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """
    Log in to your TaskNode account.
    """
    return auth.login(email, password)


@app.command()
def signup(
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True),
):
    """
    Sign up for a TaskNode account.
    """
    return auth.signup(email, password)


@app.command()
def logout():
    """
    Log out of your TaskNode account.
    """
    return auth.logout()


@app.command()
def resend_verification(email: str = typer.Option(..., prompt=True)):
    """
    Resend the email verification code to your email address.
    """
    return auth.resend_verification(email)


@app.command()
def reset_password(
    email: str = typer.Option(..., prompt=True),
):
    """
    Reset your account password.
    """
    return auth.reset_password(email)


@app.command()
def whoami():
    """
    Show information about the currently logged in user.
    """
    return auth.whoami()


@app.command()
def submit(
    script: str = typer.Argument(
        ...,
        help="The Python script or Jupyter notebook to run (relative to the current directory, for example 'script.py', 'path/to/script.py', or 'notebook.ipynb')",
    ),
):
    """
    Submit a Python script or Jupyter notebook to be run in the cloud.
    """
    # Normalize path separators before passing to tasks.submit
    script = script.replace("\\", "/")
    return tasks.submit(script)


@app.command()
def list_jobs(offset: int = typer.Option(0, "--offset", "-o", help="Number of jobs to skip")):
    """
    List your TaskNode jobs and their statuses.
    """
    return tasks.list_jobs(offset)


if __name__ == "__main__":
    app()
