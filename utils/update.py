from time import gmtime, strftime
from os import system, walk

from post import Post


now = gmtime()

with open("templates/master.html", "r") as f:
    template = f.read() % now.tm_year

with open("templates/error.html", "r") as f:
    errtemplate = f.read()

with open("templates/map.html", "r") as f:
    maptemplate = f.read()

errors = {
    404: "File Not Found"
}

posts: list[Post] = []
for path, dirs, files in walk("posts"):
    for file in files:
        if file.endswith(".json"):
            posts.append(Post.fromJSON(f"posts/{file}"))


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

    content = "\n            <article>"
    for p in reversed(posts):
        content += f"\n                <ul>\n                    <li>\n                        <a href=\"/{p.path}\">{p.title}</a> ({strftime(r'%Y-%m-%d', p.date)})\n                    </li>\n                </ul>"

    with open("posts.html", "w") as f:
        content += "\n            </article>"
        css = "\n        " + "\n        ".join([f"<link rel=\"stylesheet\" href=\"{cssfile}\">" for cssfile in set(styles)])

        f.write(template.format(page="Posts", css=css, content=content))

    system("http-server -p 80 -d false -e html -c-1") # for testing