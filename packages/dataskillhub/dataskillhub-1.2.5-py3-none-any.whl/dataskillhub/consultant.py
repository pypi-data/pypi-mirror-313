from pathlib import Path
from .cv import CV
from .init_src import create_folder
from .extract import get_dcs


consultants_path = "consultants"
config_path = "config"
template_path = "templates"


def make_cvs(dc_list, output_path, asset_path_html, asset_path_pdf, consultant, consultant_path_html, consultant_path_pdf):  # noqa:
    create_folder(f"{output_path}/{consultant}")
    for dc in dc_list:
        cv = CV(
            dossier_competence=dc,
            cv_template_path=f"{template_path}/index.html",
            anonymous_doc_path=f"{config_path}/anonyme.json",
        )
        output_path_name = f"{output_path}/{consultant}/{dc.file_id}"  # noqa:
        if dc.anonyme is True:
            cv.make_html(output_path_name, asset_path_html, consultant_path_html, "anonyme", anonimize=True)  # noqa:
            cv.make_pdf(output_path_name, asset_path_pdf, consultant_path_pdf, "anonyme", anonimize=True)  # noqa:
        else:
            cv.make_html(output_path_name, asset_path_html, consultant_path_html, "normal", anonimize=False)  # noqa:
            cv.make_pdf(output_path_name, asset_path_pdf, consultant_path_pdf, "normal", anonimize=False)  # noqa:


def export_consultant(consultant, output_path, asset_path_html, asset_path_pdf,consultant_path_html):  # noqa:
    consultant_path_pdf = f"{consultants_path}/{consultant}"
    dcs = get_dcs(consultants_path, consultant)
    make_cvs(dcs, output_path, asset_path_html, asset_path_pdf, consultant, consultant_path_html,consultant_path_pdf) # noqa:


def get_consultants():
    consultant_list = []
    path = Path(consultants_path)
    for i in path.iterdir():
        consultant_list.append(i.name)
    return consultant_list


def add_consultant(consultant: str):
    folder_path = Path(f"{consultants_path}/{consultant}")
    folder_path.mkdir(parents=True, exist_ok=True)


def check_consultant(consultant: str):
    file_miss = False
    file_list = [
        "export.yml",
        "valeur_ajoutee.md",
        "competences_cles.md",
        "diplomes.md",
        "certifications_formations.md",
        "langues.md",
        "animateur.md",
        "missions_significatives.md",
    ]
    for f in file_list:
        path = Path(f"{consultants_path}/{consultant}/{f}")
        if not path.exists():
            file_miss = True
            print(f"{f} is missing.")
    if not file_miss:
        print("All files exist.")
