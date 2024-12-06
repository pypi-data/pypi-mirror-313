"""
E2Clab error module
"""

from pathlib import Path


class E2clabError(Exception):
    pass


class E2clabFileError(E2clabError):
    def __init__(self, file_path: Path, desc: str) -> None:
        self.msg = f"Error loadding E2cLab configuration file '{file_path}': {desc}"
        super().__init__(self.msg)


class E2clabConfigError(E2clabError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
