import click

from . import fediverse_features_archive, load_config


@click.command
@click.option("--list", is_flag=True, default=False, help="Lists available features")
@click.option("--tag", help="Overwrites the default from fediverse-features.toml")
@click.option(
    "--gitignore",
    is_flag=True,
    default=False,
    help="Adds target directory to .gitignore if not present",
)
def features(list, tag, gitignore):
    config = load_config()
    if not tag:
        tag = config.tag

    with fediverse_features_archive(tag) as archive:
        if list:
            print("Available feature files")
            for filename in archive.namelist():
                if filename.endswith(".feature"):
                    print(filename)
        else:
            for name in config.features:
                archive.extract(name, config.target)


if __name__ == "__main__":
    features()
