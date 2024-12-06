"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """LeadLog."""


if __name__ == "__main__":
    main(prog_name="leadlog")  # pragma: no cover
