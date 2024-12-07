import typer


class TyperPrint:  # pragma: no cover
    @staticmethod
    def info(msg: str, with_newline=True) -> None:
        typer.secho(msg, fg=typer.colors.BLUE, nl=with_newline)

    @staticmethod
    def success(msg: str, with_newline=True) -> None:
        typer.secho(msg, fg=typer.colors.GREEN, nl=with_newline, bold=True)

    @staticmethod
    def error(msg: str, with_newline=True) -> None:
        typer.secho(msg, fg=typer.colors.RED, nl=with_newline, bold=True)

    @staticmethod
    def warning(msg: str, with_newline=True) -> None:
        typer.secho(msg, fg=typer.colors.YELLOW, nl=with_newline)
