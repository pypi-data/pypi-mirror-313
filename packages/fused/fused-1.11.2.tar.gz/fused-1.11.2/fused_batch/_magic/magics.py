from __future__ import annotations

import shlex
from typing import TYPE_CHECKING, List, Optional

import click
from IPython.core.magic import Magics, line_magic, magics_class

from fused_batch._global_api import get_api
from fused_batch.models.schema import Field, Schema

if TYPE_CHECKING:
    from IPython.core.interactiveshell import InteractiveShell


@click.command()
@click.argument("udf_name", type=str, required=True)
def load_udf_line_parser():
    """Define a user-defined function template"""
    pass


@magics_class
class FusedMagics(Magics):
    fused_shell: InteractiveShell

    def __init__(self, shell: InteractiveShell):
        self.fused_shell = shell
        super().__init__(shell)

    @staticmethod
    def parse_fields(fields: List[str]) -> Optional[Schema]:
        if len(fields) == 0:
            return None

        parsed_fields: List[Field] = []
        for field in fields:
            split = field.split(":", maxsplit=1)
            if len(split) == 1:
                raise NotImplementedError()

            name = split[0]
            dtype = split[1]
            parsed_field = Field(name=name, type=dtype)  # type: ignore
            parsed_fields.append(parsed_field)

        return Schema(fields=parsed_fields)

    @line_magic
    def load_job(self, line: str) -> None:
        job_name = line.strip()
        job_step_config = get_api().get_job_config(job_name)._to_job_step_config()
        job_step_config.render()

    @line_magic
    def load_udf(self, line: str) -> None:
        ctx = click.Context(load_udf_line_parser)
        parser = load_udf_line_parser.make_parser(ctx)
        shell_split_args = self._split_args(line)
        values, _args, _order = parser.parse_args(shell_split_args)

        help_text = load_udf_line_parser.get_help(ctx)

        # Handle --help.
        should_show_help = "help" in values.keys() and values["help"] is True
        if should_show_help:
            print(help_text)
            return

        # We don't use .get() here because udf_name defaults to None
        udf_name = values.get("udf_name") or ""
        udf_name = udf_name.strip()
        if udf_name == "":
            raise ValueError(
                f"No name was passed for the user-defined function.\n\n{help_text}"
            )

        udf = eval(udf_name, self.fused_shell.user_global_ns, self.fused_shell.user_ns)
        udf.render()

    def _split_args(self, line: str) -> List[str]:
        """Split arguments using shell style splitting.

        This is needed beyond splitting on whitespace so that arguments
        containing whitespace can be passed in. It also makes comments (#)
        behave as expected."""
        return shlex.split(line, comments=True)


def load_ipython_extension(ipython: InteractiveShell):
    magics = FusedMagics(ipython)
    ipython.register_magics(magics)
