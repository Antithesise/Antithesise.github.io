from json import dump, load

from typing import Self


with open("templates/project.html", "r") as f:
    template = f.read()


class Project:
    title: str
    assets: str
    description: str

    def __init__(self, title: str="", description: str="") -> None:
        self.title = title
        self.asstes = []
        self.description = description

    @classmethod
    def fromJSON(cls, path: str) -> Self:
        p = cls()

        with open(path, "r") as f:
            data = load(f)

        p.title = data["title"]
        p.assets = data["assets"]
        p.description = data["description"]

        return p

    def toJSON(self, path: str="") -> None:
        with open((path or f"projects/{self.title.replace(' ', '_')}.json"), "w") as f:
            dump({
                "title": self.title,
                "assets": self.assets,
                "description": self.description
            }, f, indent=4)

    def toHTML(self) -> str:
        assets = ""

        if self.assets:
            assets += "\n                            "

            assets += "\n                            ".join([f"<li><a href={a}>{a}</a></li>" for a in self.assets])

        return template.format(
            assets=assets,
            title=self.title,
            description=self.description
        )

if __name__ == "__main__":
    Project(input("Project Title: ")).toJSON()