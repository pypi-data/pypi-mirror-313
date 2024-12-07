import click

from fused._auth import authenticate as _authenticate
from fused.api import logout as _logout


@click.group()
def main():
    pass


@main.command()
def authenticate():
    _authenticate()


@main.command()
def logout():
    _logout()


if __name__ == "__main__":
    main()
