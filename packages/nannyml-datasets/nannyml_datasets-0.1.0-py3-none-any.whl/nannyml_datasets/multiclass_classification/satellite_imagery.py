import os

from nannyml_datasets.constants import GITHUB_DATASETS_REPO
from nannyml_datasets.typing import Dataset
from nannyml_datasets.multiclass_classification.typing import _Dataset


REMOTE_FILE_SOURCE = os.path.join(
    GITHUB_DATASETS_REPO, "multiclass_classification", "satellite_imagery"
)
COLUMN_MAPPING = {
    "predictions_column_name": "y_pred",
    "predicted_probabilities_column_names": {
        "0": "pred_proba_0",
        "1": "pred_proba_1",
        "2": "pred_proba_2",
        "3": "pred_proba_3",
    },
    "targets_column_name": "y_true",
    "timestamps_column_name": "timestamp",
    "continuous_feature_column_names": [f"feature_{i+1}" for i in range(1000)],
    "categorical_feature_column_names": [],
    "excluded_column_names": [],
}


class SatelliteImageryDataset(Dataset):
    """"""

    def __init__(self):
        super().__init__(
            reference_dataset=_Dataset(
                remote_file_name="reference_image_satellite.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
            monitoring_dataset=_Dataset(
                remote_file_name="analysis_image_satellite.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
        )


satellite_imagery = SatelliteImageryDataset()
