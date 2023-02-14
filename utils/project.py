from json import dump, load

from typing import Self


with open("templates/project.html", "r") as f:
    template = f.read()


class Project:
    title: str
    path: str
    description: str

    def __init__(self, title: str="", description: str="") -> None:
        self.title = title
        self.path = f"projects/{title}.zip"
        self.description = description

    @classmethod
    def fromJSON(cls, path: str) -> Self:
        p = cls()

        with open(path, "r") as f:
            data = load(f)

        p.title = data["title"]
        p.path = data["path"]
        p.description = data["description"]

        return p

    def toJSON(self, path: str="") -> None:
        with open((path or self.path + ".json"), "w") as f:
            dump({
                "title": self.title,
                "path": self.path,
                "description": self.description
            }, f, indent=4)

    def toHTML(self) -> str:
        return template.format(
            path=self.path,
            title=self.title,
            description=self.description
        )

if __name__ == "__main__":
    Project(input("Project Title: ")).toJSON()