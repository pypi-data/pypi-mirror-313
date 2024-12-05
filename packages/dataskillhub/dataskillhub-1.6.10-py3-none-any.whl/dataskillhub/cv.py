from weasyprint import HTML, CSS
import json
from .extract import DossierCompetence, Section, get_content
from jinja2 import Template
import markdown

config_path = "config"
template_path = "templates"


class CV:
    """class pour manipuler un contenu du cv"""

    def __init__(
        self,
        dossier_competence: DossierCompetence,
        cv_template_path=f"{template_path}/index.html",
        anonymous_doc_path=f"{config_path}/anonyme.json",
    ) -> None:
        """initialize the content of the CV"""
        cv_template = get_content(cv_template_path)
        self.dossier_competence = dossier_competence
        self.template = Template(cv_template)
        self.anonymous_doc = get_content(anonymous_doc_path)

    def template_render(self, asset_path: str, consultant_path: str, version: str):  # noqa:
        """Convert md to html and fill it into template"""
        body_dict = self.dossier_competence.body
        for key in body_dict:
            body_dict[key] = Section(
                title=body_dict[key].title,
                content=markdown.markdown(body_dict[key].content),
            )
        content_filled = self.template.render(
            asset_path=asset_path,
            consultant_path=consultant_path,
            identity=self.dossier_competence.identity,
            post=self.dossier_competence.post,
            version=version,
            **body_dict,
            certifs=self.dossier_competence.certifs
        )
        return content_filled

    def anonimize(self, cv: str) -> str:
        """Anonymization requested text"""
        anonimization_dict = json.loads(self.anonymous_doc)
        for key in anonimization_dict:
            cv = cv.replace(key, anonimization_dict[key])
        return cv

    def make_html(self, output_path_name, asset_path, consultant_path, version, anonimize: bool):  # noqa:
        """make cv in html"""
        content_filled = self.template_render(asset_path, consultant_path , version)  # noqa:
        if anonimize:
            content_filled = self.anonimize(content_filled)
        output_path_name = output_path_name + ".html"
        with open(output_path_name, "w", encoding="utf-8") as html_file_output:
            html_file_output.write(content_filled)

    def make_pdf(self, output_path_name, asset_path, consultant_path, version, anonimize: bool):  # noqa:
        """make cv in pdf"""
        content_filled = self.template_render(asset_path, consultant_path, version)  # noqa:
        if anonimize:
            content_filled = self.anonimize(content_filled)
        output_path_name = output_path_name + ".pdf"
        with open(f"{asset_path}/style.css", "rb") as css:
            css_content = css.read()
        HTML(string=content_filled, base_url="").write_pdf(
            output_path_name,
            stylesheets=[CSS(string=css_content)],
            presentational_hints=True,
        )
