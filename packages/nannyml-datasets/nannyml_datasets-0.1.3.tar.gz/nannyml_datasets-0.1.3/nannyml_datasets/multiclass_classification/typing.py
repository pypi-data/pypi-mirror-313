from typing import Dict, List, Optional
import numpy.typing as npt
from nannyml_datasets.typing import _Dataset as _BaseDataset


ClassLabel = str


class _Dataset(_BaseDataset):
    def __init__(
        self,
        remote_file_name: str,
        remote_file_source: str,
        continuous_feature_column_names: Optional[List[str]] = None,
        categorical_feature_column_names: Optional[List[str]] = None,
        remote_file_checksum: Optional[str] = None,
        predicted_probabilities_column_names: Optional[Dict[ClassLabel, str]] = None,
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

        self.predicted_probabilities_column_names = predicted_probabilities_column_names

    @property
    def predicted_probabilities(self) -> Dict[ClassLabel, npt.NDArray]:
        return {
            class_label: self.data[column_name].to_numpy()
            for class_label, column_name in self.predicted_probabilities_column_names.items()
        }

    @property
    def classes(self) -> List[ClassLabel]:
        return list(sorted(self.predicted_probabilities_column_names.keys()))
