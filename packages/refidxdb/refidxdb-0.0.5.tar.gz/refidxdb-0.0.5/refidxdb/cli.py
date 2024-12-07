# Guide: https://medium.com/clarityai-engineering/how-to-create-and-distribute-a-minimalist-cli-tool-with-python-poetry-click-and-pipx-c0580af4c026
import sys
from pathlib import Path

import click
import plotext as plt
import polars as pl
from streamlit import runtime
from streamlit.web import cli as stcli

from refidxdb import Aria, RefIdx, RefIdxDB, databases


@click.group()
def cli() -> None:
    pass


@cli.command(
    help="""Manage databases.
    Use commas for multiple entries.
    The input `all` processes all available databases."""
)
@click.option(
    "--download",
    help="Download provided databases.",
)
@click.option(
    "--clean",
    help="Remove provided databases.",
)
def db(download, clean) -> None:
    if download is not None:
        download_db(download)
    if clean is not None:
        raise Exception("Cleaning is not yet implemented.")


def download_db(dbs: str):
    if dbs == "all":
        download_list = list(databases.values())
    else:
        db_list = [item.lower() for item in dbs.split(",")]
        download_list = [databases[item] for item in db_list]

    for Source in download_list:
        db = Source()
        db.download()

    click.echo("All databases downlaoded!")
    click.echo("Bye :)")


@cli.command(help="""Display data from a database.""")
@click.option(
    "--db",
    help="Database to be used.",
)
@click.option(
    "--data",
    help="Data to be used from the database.",
)
@click.option(
    "--display",
    default="table",
    show_default=True,
    help="How to display the data: table or graph.",
)
@click.option(
    "--bounds",
    help="Bounds for the graph. Two values separated by a comma, e.g., `1.5,3.56`",
)
def show(db, data, display, bounds) -> None:
    df = parse_source(db, data)
    nk = df.nk.with_columns(pl.col("w").truediv(df.scale))
    if bounds is not None:
        bounds = [float(val) for val in bounds.split(",")]
        if len(bounds) != 2:
            raise Exception("Bounds need to have two values separated by a comma.")
        nk = nk.filter((pl.col("w") > bounds[0]) & (pl.col("w") < bounds[1]))
    match str.lower(display):
        case "table":
            with pl.Config(tbl_rows=1000):
                click.echo(nk)
        case "graph":
            if "n" in df.nk.columns:
                plt.plot(nk["w"], nk["n"], label="n")
            if "k" in df.nk.columns:
                plt.plot(nk["w"], nk["k"], label="k")
            plt.title("Refractive index values")
            plt.xlabel(f"Wavelength in {df.scale}")
            plt.ylabel("Values")
            plt.show()
        case _:
            raise Exception("Unsupported display option")


def parse_source(db, data) -> RefIdxDB:
    match str.lower(db):
        case "refidx":
            return RefIdx(data)
        case "aria":
            return Aria(data)
        case _:
            raise Exception(f"Provided {db} is not supported!")


@cli.command(help="""Explore data using Streamlit""")
def explore():
    if not runtime.exists():
        print(Path(__file__).parent)
        sys.argv = ["streamlit", "run", f"{Path(__file__).parent}/app.py"]
        sys.exit(stcli.main())
