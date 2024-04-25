from dataclasses import dataclass, fields, field


@dataclass
class Config:
    is_installed: bool = False
    crossref_url: str = 'https://api.crossref.org/works/'
    unpay_pdfs_url: str = 'https://api.unpaywall.org/v2'


@dataclass
class DefaultVal:
    val: str = field(default_factory=str)


@dataclass
class NoneRef:
    def __post_init__(self):
        for field in fields(self):
            if isinstance(field.default, DefaultVal):
                field_val = getattr(self, field.name)
                if isinstance(field_val, DefaultVal) or field_val is None:
                    setattr(self, field.name, field.default.val)


@dataclass
class CrossRefItem(NoneRef):
    is_installed: bool
    title: str = field(default_factory=str)
    text: str = field(default_factory=str)
    type: str = field(default_factory=str)
    author: str = field(default_factory=str)
    container_title: str = field(default_factory=str)
    date: str = field(default_factory=str)
    DOI: str = field(default_factory=str)
    ISSN: str = field(default_factory=str)
    page: str = field(default_factory=str)
    volume: str = field(default_factory=str)
    issue: str = field(default_factory=str)


@dataclass
class SciItem:
    file_url: str
    DOI: str
    file_path: str