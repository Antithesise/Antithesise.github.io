from time import gmtime, strftime
from os import walk

from post import Post


now = gmtime()

template = """
<!DOCTYPE html>
<html lang="en" dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>{page} | GoodCoderBBoy's Blog</title>
        <link rel="stylesheet" href="/css/style.css">
        <link rel="icon" href="/media/Avatar.jpeg" />
    </head>
    <body>
        <header>
            <h1 id="title"><a href="/">GoodCoderBBoy</a></h1>
            <img id="icon" src="/media/Avatar.jpeg">
            <nav></nav>
        </header>
        <aside>
            <ul>
                <li>
                    <a href="/posts">all posts</a>
                </li>
            </ul>
        </aside>
        <main>{content}
        </main>
        <footer>
            <span id="copyright">&copy; %d GoodCoderBBoy</span>
        </footer>
    </body>
</html>
""".strip() % now.tm_year

posts: list[Post] = []
for path, dirs, files in walk("posts"):
    for file in files:
        if file.endswith(".json"):
            posts.append(Post.fromJSON(f"posts/{file}"))


if __name__ == "__main__":
    home = []

    for p in posts:
        content = p.toHTML()

        home.insert(0, content)

        with open(f"{p.path}.html", "w") as f:
            f.write(template.format(page=p.title, content=content))

    with open("index.html", "w") as f:
        f.write(template.format(page="Home", content="".join(home[:50])))

    content = "\n            <article>"
    for p in reversed(posts):
        content += f"\n                <ul>\n                    <li>\n                        <a href=\"/{p.path}\">{p.title}</a> ({strftime(r'%Y-%m-%d', p.date)})\n                    </li>\n                </ul>"

    with open("posts.html", "w") as f:
        content += "\n            </article>"

        f.write(template.format(page="Posts", content=content))