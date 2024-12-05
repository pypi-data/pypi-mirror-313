from pathlib import Path
import click
from .consultant import (
    export_consultant,
    get_consultants,
    add_consultant,
    check_consultant,
)
from .init_src import copy_file, create_folder


@click.group()
def main():
    pass


@main.command()
def init():
    folder_list = ["assets", "templates", "config", "consultants"] # noqa
    for folder in folder_list:
        create_folder(f"{folder}/")
    code_path = Path(__file__).parent
    copy_file(code_path / "assets", "assets", "logo_datalyo.png")  # noqa
    copy_file(code_path / "assets", "assets", "logo.png")  # noqa
    copy_file(code_path / "assets", "assets", "icon_chat.png")  # noqa
    copy_file(code_path / "assets", "assets", "icon_diploma.png")  # noqa
    copy_file(code_path / "assets", "assets", "icon_person.png")  # noqa
    copy_file(code_path / "assets", "assets", "icon_skill.png")  # noqa
    copy_file(code_path / "assets", "assets", "icon_star.png")  # noqa
    copy_file(code_path / "assets", "assets", "cert_psm.svg") # noqa
    copy_file(code_path / "assets", "assets", "cert_tableau.png")  # noqa
    copy_file(code_path / "assets", "assets","cert_talend.png")  # noqa
    copy_file(code_path / "assets", "assets", "style.css")
    copy_file(code_path / "templates", "templates", "index.html")  # noqa
    copy_file(code_path / "config", "config", "anonyme.json")  # noqa
    copy_file(code_path / "config", "config", "sections.yml")  # noqa
    print("fichiers prêts")


@main.group()
def consultant():
    pass


@consultant.command()
@click.argument("consultant")
@click.option("--output_path", default="outputs", help="Where to place the cvs")  # noqa:
@click.option("--asset_path_html", default="../../assets", help="Where the assets for html stock")  # noqa:
@click.option("--asset_path_pdf", default="assets", help="Where the assets for pdf stock") # noqa:
@click.option("--consultant_path_html", default=".", help="Where the avatar of consultant for html stock")  # noqa: 
def export(consultant, output_path="outputs",
           asset_path_html="../../assets", asset_path_pdf="assets",
           consultant_path_html="."): # noqa:
    if consultant == "all":
        consultant_list = get_consultants()
        for consul in consultant_list:
            export_consultant(
                consul, output_path, asset_path_html, asset_path_pdf, consultant_path_html)  # noqa:
    else:
        export_consultant(
            consultant, output_path, asset_path_html, asset_path_pdf, consultant_path_html)  # noqa:


@consultant.command()
def list():
    for consultant in get_consultants():
        print(consultant)


@consultant.command()
@click.argument("consultant")
def new(consultant):
    add_consultant(consultant)


@consultant.command()
@click.argument("consultant")
def check(consultant):
    check_consultant(consultant)


if __name__ == "__main__":
    main()
