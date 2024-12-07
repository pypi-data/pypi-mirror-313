import os

from nannyml_datasets.constants import GITHUB_DATASETS_REPO
from nannyml_datasets.typing import Dataset
from nannyml_datasets.binary_classification.typing import _Dataset


REMOTE_FILE_SOURCE = os.path.join(
    GITHUB_DATASETS_REPO, "binary_classification", "hotel_booking"
)
COLUMN_MAPPING = {
    "predictions_column_name": "y_pred",
    "predicted_probabilities_column_name": "y_pred_proba",
    "targets_column_name": "is_canceled",
    "timestamps_column_name": "timestamp",
    "continuous_feature_column_names": [
        "adr",
        "adults",
        "babies",
        "booking_changes",
        "children",
        "days_in_waiting_list",
        "lead_time",
        "parking_spaces",
        "previous_bookings_not_canceled",
        "previous_cancellations",
        "stays_in_weekend_nights",
        "stays_in_week_nights",
        "total_of_special_requests",
    ],
    "categorical_feature_column_names": [
        "agent",
        "assigned_room_type",
        "company",
        "country",
        "customer_type",
        "deposit_type",
        "distribution_channel",
        "hotel",
        "market_segment",
        "meal",
        "reserved_room_type",
    ],
    "excluded_column_names": ["index"],
}


class HotelBookingDataset(Dataset):
    """"""

    def __init__(self):
        super().__init__(
            reference_dataset=_Dataset(
                remote_file_name="reference_hotel_booking.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
            monitoring_dataset=_Dataset(
                remote_file_name="monitoring_hotel_booking.parquet",
                remote_file_source=REMOTE_FILE_SOURCE,
                **COLUMN_MAPPING,
            ),
        )


hotel_booking = HotelBookingDataset()
