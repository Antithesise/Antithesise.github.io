from time import localtime, mktime, strftime, struct_time
from json import dump, load

from typing import Self


with open("templates/post.html", "r") as f:
    template = f.read()


class Post:
    title: str
    path: str
    date: struct_time
    loc: str
    css: list[str]
    content: str

    def __init__(self, title: str="", loc: str="", css: list[str]=[], content: str="") -> None:
        now = localtime()

        self.title = title
        self.path = "posts/%d-%s-" % (now.tm_year, str(now.tm_mon).zfill(2))
        self.date = now
        self.loc = loc
        self.css = css
        self.content = content

    @classmethod
    def fromJSON(cls, path: str) -> Self:
        p = cls()

        with open(path, "r") as f:
            data = load(f)

        p.title = data["title"]
        p.path = data["path"]
        p.date = localtime(data["date"])
        p.loc = data["loc"]
        p.css = data["css"]
        p.content = data["content"]

        return p

    def toJSON(self, path: str="") -> None:
        with open((path or self.path + ".json"), "w") as f:
            dump({
                "title": self.title,
                "path": self.path,
                "date": int(mktime(self.date)),
                "loc": self.loc,
                "css": self.css,
                "content": self.content
            }, f, indent=4)

    def toHTML(self) -> str:
        return template.format(
            path=self.path,
            title=self.title,
            fdate=strftime(r"%Y-%m-%d %H:%M:%S", self.date),
            date=strftime(r"%I:%M %p, %Y-%m-%d", self.date),
            sep="<span>, </span>" * bool(self.loc),
            loc=self.loc,
            content=self.content.replace("\n", "\n                ")
        )

if __name__ == "__main__":
    Post()