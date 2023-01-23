from os import walk

from typing import Any, Callable, Literal, NamedTuple, Optional, overload


class FormattedDirectory(NamedTuple):
    dirs: list[str]
    files: list[str]

class Directory(NamedTuple):
    dirs: list[str]
    files: list[str]


@overload
def index(dirpath: str, template: Optional[str]=None, /, *args: Any, filter: Callable[[str], bool]=..., format: Literal[True]=..., **kwargs: Any) -> FormattedDirectory: ...

@overload
def index(dirpath: str, template: Optional[str]=None, /, *args: Any, filter: Callable[[str], bool]=..., format: Literal[False]=..., **kwargs: Any) -> Directory: ...

def index(dirpath, template=None, /, *args, filter: Callable[[str], bool]=lambda p: p != "index.html", format=True, **kwargs):
    dirpath = dirpath.rstrip("\\/")

    if template is None and format is True:
        raise ValueError("template must be provided if format is True.")

    elif template is None:
        template = ""

    else:
        with open(template, "r") as f:
            template = f.read() % args

    dirlist, filelist = [], []
    for path, dirs, files in walk(dirpath + "/"):
        dirlist = [dir for dir in dirs if filter(dir)]
        filelist = [file for file in files if filter(file)]

    dirlist.insert(0, "..")

    if format:
        dirlist = list(map(lambda p: template.format(path=dirpath, file=p + "/", **kwargs), dirlist))
        filelist = list(map(lambda p: template.format(path=dirpath, file=p, **kwargs), filelist))

        return FormattedDirectory(dirlist, filelist)

    else:
        dirlist = list(map(lambda p: dirpath + "/" + p, dirlist))
        filelist = list(map(lambda p: dirpath + "/" + p, filelist))

        return Directory(dirlist, filelist)