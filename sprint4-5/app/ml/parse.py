from app.schemas.inference import InferenceIn
import pandas as pd
from numpy.typing import NDArray
import re


class DataMapper:
    def __init__(self, csv_path: str):
        """Inicializa a classe com o caminho do CSV e gera os mapeamentos."""
        self.csv_path = csv_path
        self.mappings = self._generate_mappings()

    def _generate_mappings(self) -> dict:
        """Gera mapeamentos de colunas categóricas para valores numéricos."""
        hotel_df = pd.read_csv(self.csv_path)
        hotel_df.drop(columns=["Booking_ID"], inplace=True)

        mappings = {
            column: {
                value_key: associeted_number
                for associeted_number, value_key in enumerate(
                    sorted(
                        hotel_df[column].unique(),
                        key=lambda x: (self.extract_number(x), x),
                    )
                )
            }
            for column in hotel_df.columns
            if hotel_df[column].dtype == "object"
        }

        return mappings

    def extract_number(self, key: str) -> int:
        """Extrai números das chaves."""
        match = re.search(r"\d+", key)

        return int(match.group()) if match else float("inf")

    def apply_mapping(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica os mapeamentos ao DataFrame fornecido."""
        for column, mapping in self.mappings.items():
            df[column] = df[column].map(mapping)

        return df

    def parse(self, obj: "InferenceIn") -> NDArray:
        """Faz o parse de um objeto `InferenceIn` para `NDArray`."""
        input_data = pd.DataFrame([obj.model_dump()])
        input_data = self.apply_mapping(input_data)

        return input_data.values


Mapper = DataMapper("app/ml/dataset/HotelReservations.csv")
