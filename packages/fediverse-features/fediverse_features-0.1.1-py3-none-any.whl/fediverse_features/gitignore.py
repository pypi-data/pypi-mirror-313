import pathlib


def ensure_in_gitignore(target: str, gitignore_filename: str = ".gitignore"):
    if pathlib.Path(gitignore_filename).exists():
        with open(gitignore_filename, "r") as fp:
            data = fp.readlines()

        need_new_line = data[-1][-1] != "\n"

        if target in data or f"{target}\n" in data:
            return

    else:
        need_new_line = False

    with open(gitignore_filename, "a") as fp:
        if need_new_line:
            fp.write("\n")
        fp.write(target + "\n")
