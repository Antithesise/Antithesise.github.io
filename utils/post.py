from time import gmtime, strftime, struct_time, time
from json import load

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

    @classmethod
    def fromJSON(cls, path: str) -> Self:
        p = cls()

        with open(path, "r") as f:
            data = load(f)

        p.title = data["title"]
        p.path = data["path"]
        p.date = gmtime(data["date"])
        p.loc = data["loc"]
        p.css = data["css"]
        p.content = data["content"]

        return p

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
    now = gmtime()

    with open("posts/%d-%s-.json" % (now.tm_year, str(now.tm_mon).zfill(2)), "w") as f:
        f.write("{\n    \"title\": \"\",\n    \"path\": \"posts/%d-%s-\",\n    \"date\": %d,\n    \"loc\": \"\",\n    \"css\": [],\n    \"content\": \"\"\n}" % (now.tm_year, str(now.tm_mon).zfill(2), int(time())))