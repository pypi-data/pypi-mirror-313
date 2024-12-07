import os

from nannyml_datasets.constants import GITHUB_DATASETS_REPO
from nannyml_datasets.typing import Dataset
from nannyml_datasets.binary_classification.typing import _Dataset


REMOTE_FILE_SOURCE = os.path.join(
    GITHUB_DATASETS_REPO, "binary_classification", "synthetic_car_loan"
)
COLUMN_MAPPING = {
    "predictions_column_name": "y_pred",
    "predicted_probabilities_column_name": "y_pred_proba",
    "targets_column_name": "repaid",
    "timestamps_column_name": "timestamp",
    "continuous_feature_column_names": [
        "car_value",
        "debt_to_income_ratio",
        "driver_tenure",
        "loan_length",
    ],
    "categorical_feature_column_names": [
        "repaid_loan_on_prev_car",
        "salary_range",
        "size_of_downpayment",
    ],
    "excluded_column_names": ["id"],
}


class SyntheticCarLoanDataset(Dataset):
    """"""

    def __init__(self):
        super().__init__(
            reference_dataset=_Dataset(
                remote_file_name="reference_synthetic_car_loan.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
            monitoring_dataset=_Dataset(
                remote_file_name="monitoring_synthetic_car_loan.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
        )


synthetic_car_loan = SyntheticCarLoanDataset()
