from __future__ import annotations
import os
import tempfile
import time
import pyarrow as pa
import pyarrow.parquet as pq
import numpy.typing as npt
import requests

from typing import Iterable, List, Mapping, Optional


class _Dataset:
    def __init__(
        self,
        remote_file_name: str,
        remote_file_source: str,
        continuous_feature_column_names: Optional[List[str]] = None,
        categorical_feature_column_names: Optional[List[str]] = None,
        remote_file_checksum: Optional[str] = None,
        predictions_column_name: Optional[str] = None,
        targets_column_name: Optional[str] = None,
        timestamps_column_name: Optional[str] = None,
        excluded_column_names: Optional[List[str]] = None,
    ):
        self.remote_file_name = remote_file_name
        self.remote_file_source = remote_file_source
        self.remote_file_checksum = remote_file_checksum
        self.continuous_feature_column_names = continuous_feature_column_names or []
        self.categorical_feature_column_names = categorical_feature_column_names or []
        self.predictions_column_name = predictions_column_name
        self.targets_column_name = targets_column_name
        self.timestamps_column_name = timestamps_column_name
        self.excluded_column_names = excluded_column_names or []

        self._data: Optional[pa.Table] = None

    @property
    def data(self) -> pa.Table:
        if self._data is None:
            with tempfile.NamedTemporaryFile() as f:
                parquet_path = download_source(
                    f,
                    self.remote_file_source,
                    self.remote_file_name,
                    self.remote_file_checksum,
                )
                self._data = pq.read_table(parquet_path)

        return self._data

    @property
    def predictions(self) -> npt.NDArray:
        assert (
            self.predictions_column_name is not None
        ), "No predictions column name provided"
        return self.data[self.predictions_column_name].to_numpy()

    @property
    def targets(self) -> npt.NDArray:
        assert self.targets_column_name is not None, "No targets column name provided"
        return self.data[self.targets_column_name].to_numpy()

    @property
    def timestamps(self) -> npt.NDArray:
        assert (
            self.timestamps_column_name is not None
        ), "No timestamps column name provided"
        return self.data[self.timestamps_column_name].to_numpy()

    @property
    def categorical_features(self) -> Iterable[npt.NDArray]:
        return (
            self.data[col].to_numpy() for col in self.categorical_feature_column_names
        )

    @property
    def continuous_features(self) -> Iterable[npt.NDArray]:
        return (
            self.data[col].to_numpy() for col in self.continuous_feature_column_names
        )

    @property
    def features(self) -> Mapping[str, npt.NDArray]:
        return {
            col: self.data[col].to_numpy()
            for col in self.categorical_feature_column_names
            + self.continuous_feature_column_names
        }


class Dataset:
    def __init__(
        self,
        reference_dataset: _Dataset,
        monitoring_dataset: _Dataset,
    ) -> None:
        self.reference_dataset = reference_dataset
        self.monitoring_dataset = monitoring_dataset

    @property
    def reference(self) -> _Dataset:
        return self.reference_dataset

    @property
    def monitoring(self) -> _Dataset:
        return self.monitoring_dataset


def download_source(
    local_file,
    remote_file_source: str,
    remote_file_name: str,
    remote_file_checksum: Optional[str] = None,
    n_retries: int = 3,
    delay: int = 3,
):
    # Perform download
    try:
        with requests.get(
            os.path.join(remote_file_source, remote_file_name)
        ) as response:
            response.raise_for_status()
            local_file.write(response.content)
    except TimeoutError:
        if n_retries == 0:
            raise

        n_retries -= 1
        time.sleep(delay)

    # Checksum verification

    return local_file.name
