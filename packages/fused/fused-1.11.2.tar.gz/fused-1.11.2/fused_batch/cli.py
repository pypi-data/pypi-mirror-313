import click

from fused_batch._auth import authenticate as _authenticate
from fused_batch.api import logout as _logout


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
