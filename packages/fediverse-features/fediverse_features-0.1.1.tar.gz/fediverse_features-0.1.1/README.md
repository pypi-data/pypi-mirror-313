# fediverse-features

This is a simple tool to download a subset of the
Gherkin features available at
[helge/fediverse-features](https://codeberg.org/helge/fediverse-features).
These enable one to BDD tests for Fediverse
applications.

## Usage

Install via

```bash
pip install fediverse-features
```

Create a toml file `fediverse-features.toml` containing

```toml
tag = "0.1.6"

features = [
    "fedi/node_info.feature"
]
```

where features is the list of feature files. Then
run

```bash
python -mfediverse_features
```

The feature files are then downloaded to the `features/fediverse-features` directory.
One can change this directory by adding a
target parameter to the configuration file,
e.g.

```toml
tag = "0.1.6"

features = [
    "fedi/node_info.feature"
]

target = "features"
```

## Further options

One can list available features via

```bash
python -mfediverse_features --list
```

By running

```bash
python -mfediverse_features --gitignore
```

one can add the target directory to the `.gitignore` file.
