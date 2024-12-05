from pydantic import BaseModel, Field
from typing import List
import yaml


class Version(BaseModel):
    name: str
    title: str
    file_id: str
    anonymised: bool

# class ExportConfig(BaseModel):
#     post: str
#     versions: List[Version]
#     certifs: List[Certif] = Field(default=[
#             Certif(name="nom du certif", path="certifs/cert_xxx.png")
#         ])


class ExportConfig(BaseModel):
    post: str
    versions: List[Version]
    certifs: List[str] = Field(default=["certifs/cert_xxx.png"])


class HeadingLevels(BaseModel):
    level: int
    label: str


class Design(BaseModel):
    title: str
    headingLevels: List[HeadingLevels]


class Section(BaseModel):
    title: str
    content: str


class DossierCompetence(BaseModel):
    identity: str
    anonyme: bool
    post: str
    body: dict[str, Section]
    file_id: str
    certifs: List[str]


def get_content(source: str) -> str:
    """Read source file contents"""
    with open(source, "r") as content:
        content_str = content.read()
    return content_str


def read_yaml(file_path: str) -> ExportConfig:
    """Read yaml file contents"""
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return ExportConfig(**config)


def read_yaml_section(file_path: str) -> dict:
    """Read yaml file contents"""
    with open(file_path, "r") as stream:
        config = yaml.safe_load(stream)
    return config


def flat_export(
    config_section: dict, config: ExportConfig, consultant_path: str
) -> list:
    """export to list[DossierCompetence]"""
    body_dict = {}
    for id, section in config_section.items():
        s = Section(
            title=section.get("title"), content=f"{consultant_path}/{id}.md"
        )  # noqa
        body_dict[id] = s
    certifs = []
    for certif in config.certifs:
        certifs.append(certif)
    dc_list = []
    for version in config.versions:
        dc_list.append(
            DossierCompetence(
                identity=version.name,
                anonyme=version.anonymised,
                post=config.post,
                body=body_dict,
                file_id=version.file_id,
                certifs=certifs
            )  # noqa
        )
    return dc_list


def get_dcs(consultants_path: str, consultant: str) -> list:
    """read all file md in list[DossierCompetence]"""
    consultant_path = f"{consultants_path}/{consultant}"
    config = read_yaml(f"{consultant_path}/export.yml")
    config_section = read_yaml_section("config/sections.yml")
    dc_list = flat_export(config_section, config, consultant_path)
    for dc in dc_list:
        for key in dc.body:
            dc.body[key] = Section(
                title=dc.body[key].title,
                content=get_content(dc.body[key].content),  # noqa
            )
    return dc_list
