import tempfile
from typing import Tuple
import pytest

from nannyml_datasets.typing import download_source, _Dataset


@pytest.fixture
def remote_source() -> Tuple[str, str, str]:
    return (
        "https://github.com/NannyML/sample_datasets/raw/refs/heads/main/image_satellite_dataset/",
        "reference_image_satellite.parquet",
        "1234",
    )


def dataset() -> _Dataset:
    return _Dataset(
        remote_file_name="remote.parquet",
        remote_file_source="https://some-url.com/dataset/",
    )


def test_download_source_returns_path(remote_source):
    with tempfile.NamedTemporaryFile() as f:
        sut = download_source(f, *remote_source)
        assert sut == f.name
