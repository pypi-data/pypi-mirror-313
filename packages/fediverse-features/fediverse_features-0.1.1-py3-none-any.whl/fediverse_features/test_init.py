from . import fediverse_features_archive, load_config


def test_download():
    with fediverse_features_archive("0.1.6") as archive:
        feature_list = archive.namelist()

        assert len(feature_list) > 0


def test_load_config():
    config = load_config()

    assert config.tag
    assert len(config.features) > 0


def test_load_config_no_file(tmp_path):
    config = load_config(tmp_path / "test.toml")

    assert isinstance(config.features, list)
