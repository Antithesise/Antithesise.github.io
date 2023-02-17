from time import localtime, strftime, struct_time
from os import system

from index import index
from post import Post
from project import Project


now: struct_time = localtime()

with open("templates/master.html", "r") as f:
    template = f.read() % now.tm_year

with open("templates/map.html", "r") as f:
    maptemplate = f.read()

with open("templates/error.html", "r") as f:
    errtemplate = f.read()

with open("templates/autoindex.html", "r") as f:
    indextemplate = f.read()

errors = {
    404: "File Not Found"
}

indexes = [
    "css",
    "media",
    "templates",
    "utils",
]

posts = [Post.fromJSON(file) for file in index("posts", None, filter=lambda p: p.endswith(".json"), format=False).files]
projects = [Project.fromJSON(file) for file in index("projects", None, filter=lambda p: p.endswith(".json"), format=False).files]

if __name__ == "__main__":
    home = []
    styles = []

    for p in posts:
        content = "\n" + p.toHTML()
        css = "\n        " * bool(p.css) + "\n        ".join([f"<link rel=\"stylesheet\" href=\"{cssfile}\">" for cssfile in p.css])

        home.insert(0, content)
        styles += p.css

        with open(f"{p.path}.html", "w") as f:
            f.write(template.format(page=p.title, css=css, content=content))

    with open("index.html", "w") as f:
        f.write(template.format(page="Home", css="", content="".join(home[:50])))

    with open("map.html", "w") as f:
        content = f"\n            <article>\n{maptemplate}\n            </article>"

        f.write(template.format(page="Map", css="\n        <link rel=\"stylesheet\" href=\"/css/map.css\">", content=content))

    for code, message in errors.items():
        with open(f"{code}.html", "w") as f:
            content = errtemplate.format(message=message, code=code, map=maptemplate)

            f.write(template.format(page=message, css="\n        <link rel=\"stylesheet\" href=\"/css/map.css\">", content="\n" + content))

    with open("posts/index.html", "w") as f:
        content = "\n            <article>"

        for p in reversed(posts):
            content += f"\n                <ul>\n                    <li>\n                        <a href=\"/{p.path}\">{p.title}</a> ({strftime(r'%Y-%m-%d', p.date)})\n                    </li>\n                </ul>"

        content += "\n            </article>"

        css = "\n        ".join([f"<link rel=\"stylesheet\" href=\"{cssfile}\">" for cssfile in set(styles)])

        f.write(template.format(page="Posts", css=css, content=content))

    with open("projects/index.html", "w") as f:
        content = ""

        for p in projects:
            content += "\n" + p.toHTML()

        css = "\n        ".join([f"<link rel=\"stylesheet\" href=\"{cssfile}\">" for cssfile in set(styles)])

        f.write(template.format(page="Projects", css="", content=content))

    for dir in indexes:
        content = "\n" + "\n".join(["\n".join(g) for g in index(dir, "templates/file.html", filter=lambda p: p not in ["index.html", "__pycache__"])])

        content = "\n" + indextemplate.format(path=dir, content=content)

        with open(f"{dir}/index.html", "w") as f:
            f.write(template.format(page=f"{dir}/", css="\n        <link rel=\"stylesheet\" href=\"/css/index.css\">", content=content))

    system("http-server -p 80 -d false -e html -c-1") # for testing