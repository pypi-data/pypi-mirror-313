from typing import Dict


class ConfluencePage:
    def __init__(self, id: int, title: str):
        self.id: int = id
        self.title: str = title

    def __repr__(self) -> str:
        return f"ConfluencePage(id={self.id}, title='{self.title}')"


MD_to_Page = Dict[str, ConfluencePage]
