import os

from nannyml_datasets.constants import GITHUB_DATASETS_REPO
from nannyml_datasets.typing import Dataset
from nannyml_datasets.multiclass_classification.typing import _Dataset


REMOTE_FILE_SOURCE = os.path.join(
    GITHUB_DATASETS_REPO, "multiclass_classification", "synthetic_credit_card"
)
COLUMN_MAPPING = {
    "predictions_column_name": "y_pred",
    "predicted_probabilities_column_names": {
        "prepaid_card": "y_pred_proba_prepaid_card",
        "upmarket_card": "y_pred_proba_upmarket_card",
        "highstreet_card": "y_pred_proba_highstreet_card",
    },
    "targets_column_name": "y_true",
    "timestamps_column_name": "timestamp",
    "continuous_feature_column_names": [
        "app_behavioral_score",
        "requested_credit_limit",
        "credit_bureau_score",
        "stated_income",
    ],
    "categorical_feature_column_names": [
        "acq_channel",
        "app_channel",
        "is_customer",
    ],
    "excluded_column_names": ["id"],
}


class SyntheticCreditCard(Dataset):
    """"""

    def __init__(self):
        super().__init__(
            reference_dataset=_Dataset(
                remote_file_name="reference_synthetic_credit_card.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
            monitoring_dataset=_Dataset(
                remote_file_name="monitoring_synthetic_credit_card.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
        )


synthetic_credit_card = SyntheticCreditCard()
