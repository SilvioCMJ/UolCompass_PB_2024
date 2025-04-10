from pydantic import BaseModel, Field
from typing import Annotated


class InferenceIn(BaseModel):
    """Valida a entrada de dados do endpoint."""

    no_of_adults: int = Field(description="Número de adultos", ge=0, examples=[3])
    no_of_children: int = Field(description="Número de crianças", ge=0, examples=[2])
    no_of_weekend_nights: int = Field(
        description="Noites de fim de semana reservadas ou hospedadas.",
        ge=0,
        examples=[2],
    )
    no_of_week_nights: int = Field(
        description="Noites da semana reservadas ou hospedadas.",
        ge=0,
        examples=[2],
    )
    type_of_meal_plan: str = Field(
        description="Plano de refeições reservado pelo cliente.",
        max_length=12,
        examples=["Meal Plan 1"],
    )
    required_car_parking_space: int = Field(
        description="Necessidade de vaga de estacionamento (0 - Não, 1 - Sim).",
        ge=0,
        le=1,
        examples=[1],
    )
    room_type_reserved: str = Field(
        description="Tipo de quarto reservado pelo cliente.",
        max_length=11,
        examples=["Room_Type 1"],
    )
    lead_time: int = Field(
        description="Número de dias entre a data da reserva e a data de chegada",
        ge=0,
        examples=[85],
    )
    arrival_year: int = Field(
        description="Ano da data de chegada", ge=2000, examples=[2018]
    )
    arrival_month: int = Field(
        description="Mês da data de chegada", gt=0, lt=13, examples=[10]
    )
    arrival_date: int = Field(description="Data de chegada", gt=0, lt=32, examples=[23])
    market_segment_type: str = Field(
        description="Tipo do seguimento de mercado",
        max_length=13,
        examples=["Corporate", "Aviation"],
    )
    repeated_guest: int = Field(
        description="O cliente é um hóspede recorrente? (0 - Não, 1 - Sim)",
        ge=0,
        le=1,
        examples=[1],
    )
    no_of_previous_bookings_not_canceled: int = Field(
        description="Reservas anteriores não canceladas pelo cliente.",
        ge=0,
        examples=[4],
    )
    no_of_special_requests: int = Field(
        description="Total de pedidos especiais feitos pelo cliente.",
        ge=0,
        examples=[3],
    )
    booking_status: str = Field(
        description="Status indicando se a reserva foi cancelada ou não.",
        max_length=12,
        examples=["Not_Canceled"],
    )


class InferenceOut(BaseModel):
    """Valida a saída de dados do endpoint."""

    result: Annotated[
        int,
        Field(
            description="Número do resultado da previsão",
            gt=0,
            lt=4,
            examples=[1, 2, 3],
        ),
    ]
