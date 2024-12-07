from .gitignore import ensure_in_gitignore


def test_gitignore_new_file(tmp_path):
    filename = str(tmp_path / "gitignore")

    ensure_in_gitignore("features", gitignore_filename=filename)

    with open(filename) as fp:
        result = fp.readlines()

    assert len(result) == 1
    assert "features\n" in result


def test_gitignore_existing_file(tmp_path):
    filename = str(tmp_path / "gitignore")

    with open(filename, "w") as fp:
        fp.write("entry")

    ensure_in_gitignore("features", gitignore_filename=filename)

    with open(filename) as fp:
        result = fp.readlines()

    assert len(result) == 2
    assert "features\n" in result


def test_gitignore_contains_target(tmp_path):
    filename = str(tmp_path / "gitignore")

    ensure_in_gitignore("features", gitignore_filename=filename)
    ensure_in_gitignore("features", gitignore_filename=filename)

    with open(filename) as fp:
        result = fp.readlines()

    assert len(result) == 1
    assert "features\n" in result
