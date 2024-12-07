import os

from nannyml_datasets.constants import GITHUB_DATASETS_REPO
from nannyml_datasets.typing import Dataset
from nannyml_datasets.regression.typing import _Dataset


REMOTE_FILE_SOURCE = os.path.join(
    GITHUB_DATASETS_REPO, "regression", "synthetic_car_price"
)
COLUMN_MAPPING = {
    "predictions_column_name": "y_pred",
    "targets_column_name": "y_true",
    "timestamps_column_name": "timestamp",
    "continuous_feature_column_names": [
        "car_age",
        "km_driven",
        "price_new",
        "accident_count",
    ],
    "categorical_feature_column_names": [
        "door_count",
        "fuel",
        "transmission",
    ],
    "excluded_column_names": ["id"],
}


class SyntheticCarPrice(Dataset):
    """"""

    def __init__(self):
        super().__init__(
            reference_dataset=_Dataset(
                remote_file_name="reference_synthetic_car_price.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
            monitoring_dataset=_Dataset(
                remote_file_name="monitoring_synthetic_car_price.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
        )


synthetic_car_price = SyntheticCarPrice()
