import pytest
from app.application.contrib.exceptions import LoadError


@pytest.fixture
def input_data() -> dict:
    return {
        "no_of_adults": 3,
        "no_of_children": 2,
        "no_of_weekend_nights": 2,
        "no_of_week_nights": 2,
        "type_of_meal_plan": "Meal Plan 1",
        "required_car_parking_space": 1,
        "room_type_reserved": "Room_Type 1",
        "lead_time": 15,
        "arrival_year": 2023,
        "arrival_month": 10,
        "arrival_date": 23,
        "market_segment_type": "Aviation",
        "repeated_guest": 0,
        "no_of_previous_bookings_not_canceled": 2,
        "no_of_special_requests": 1,
        "booking_status": "Not_Canceled",
    }


@pytest.fixture
def mock_load_model(monkeypatch) -> None:
    def _mock_load_model():
        raise LoadError(message="Erro ao carregar o modelo do S3.")

    monkeypatch.setattr("app.ml.main.ModelHandler.load_model", _mock_load_model)
