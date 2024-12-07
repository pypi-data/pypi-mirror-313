from typing import List, Optional
from nannyml_datasets.typing import _Dataset as BaseDataset


ClassLabel = str


class _Dataset(BaseDataset):
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
        super().__init__(
            remote_file_name,
            remote_file_source,
            continuous_feature_column_names,
            categorical_feature_column_names,
            remote_file_checksum,
            predictions_column_name,
            targets_column_name,
            timestamps_column_name,
            excluded_column_names,
        )
