"""
Описание моделей данных (DTO).
"""
from typing import Optional

from datetime import datetime
from pydantic import Field, BaseModel, validator


class HashableBaseModel(BaseModel):
    """
    Добавление хэшируемости для моделей.
    """

    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))


class LocationDTO(HashableBaseModel):
    """
    Модель локации для получения сведений о погоде.

    .. code-block::

        LocationDTO(
            capital="Mariehamn",
            alpha2code="AX",
        )
    """

    capital: str
    alpha2code: str = Field(min_length=2, max_length=2)  # country alpha‑2 code


class CurrencyInfoDTO(HashableBaseModel):
    """
    Модель данных о валюте.

    .. code-block::

        CurrencyInfoDTO(
            code="EUR",
        )
    """

    code: str


class LanguagesInfoDTO(HashableBaseModel):
    """
    Модель данных о языке.

    .. code-block::

        LanguagesInfoDTO(
            name="Swedish",
            native_name="svenska"
        )
    """

    name: str
    native_name: str


class CountryDTO(BaseModel):
    """
    Модель данных о стране.

    .. code-block::

        CountryDTO(
            capital="Mariehamn",
            alpha2code="AX",
            capital_latitude=19.9348,
            capital_longitude=60.0973,
            capital_area=1580.0,
            alt_spellings=[
              "AX",
              "Aaland",
              "Aland",
              "Ahvenanmaa"
            ],
            currencies={
                CurrencyInfoDTO(
                    code="EUR",
                )
            },
            flag="http://assets.promptapi.com/flags/AX.svg",
            languages={
                LanguagesInfoDTO(
                    name="Swedish",
                    native_name="svenska"
                )
            },
            name="\u00c5land Islands",
            population=28875,
            subregion="Northern Europe",
            timezones=[
                "UTC+02:00",
            ],
        )
    """

    capital: str
    alpha2code: str
    alt_spellings: list[str]
    currencies: set[CurrencyInfoDTO]
    flag: str
    languages: set[LanguagesInfoDTO]
    name: str
    population: int
    subregion: str
    capital_latitude: float
    capital_longitude: float
    capital_area: Optional[float]
    timezones: list[str]


class CurrencyRatesDTO(BaseModel):
    """
    Модель данных о курсах валют.

    .. code-block::

        CurrencyRatesDTO(
            base="RUB",
            date="2022-09-14",
            rates={
                "EUR": 0.016503,
            }
        )
    """

    base: str
    date: str
    rates: dict[str, float]


class WeatherInfoDTO(BaseModel):
    """
    Модель данных о погоде.

    .. code-block::

        WeatherInfoDTO(
            temp=13.92,
            pressure=1023,
            humidity=54,
            wind_speed=4.63,
            description="scattered clouds",
            visibility=10000,
            timezone=3600,
            date_time=2023-03-30 12:23:34
        )
    """

    temp: float
    pressure: int
    humidity: int
    wind_speed: float
    description: str
    visibility: float
    timezone: int
    date_time: datetime


class NewsDTO(BaseModel):
    """
    Модель данных о новости.

    .. code-block::

        NewsDTO(
               title="Maia Sandu: Republica Moldova este ținta unor atacuri hibride finanțate de Kremlin. i",
               author="Ion Gaidău",
               description="Preşedinta Maia Sandu a avertizat că Republica Moldova este ținta unor atacuri hidride",
               source="Adevarul.ro",
               url="https://adevarul.ro/stiri-externe/republica-moldova/maia-sandu-republica-moldova-este-tinta-unor-
               2254533.html"
               published_at=2023-03-30T12:42:34Z,
        )
    """

    title: str
    author: Optional[str]
    description: str
    source: str
    url: str
    published_at: datetime

    # pylint: disable=E0213
    @validator("author")
    def validate_author(cls, value):  # type: ignore[no-untyped-def]
        if value is None or value == "":
            return "unknown"
        return value


class LocationInfoDTO(BaseModel):
    """
    Модель данных для представления общей информации о месте.

    .. code-block::

        LocationInfoDTO(
            location=CountryDTO(
                capital="Mariehamn",
                capital_latitude=19.9348,
                capital_longitude=60.0973,
                capital_area=1580.0,
                alpha2code="AX",
                alt_spellings=[
                  "AX",
                  "Aaland",
                  "Aland",
                  "Ahvenanmaa"
                ],
                currencies={
                    CurrencyInfoDTO(
                        code="EUR",
                    )
                },
                flag="http://assets.promptapi.com/flags/AX.svg",
                languages={
                    LanguagesInfoDTO(
                        name="Swedish",
                        native_name="svenska"
                    )
                },
                name="\u00c5land Islands",
                population=28875,
                subregion="Northern Europe",
                timezones=[
                    "UTC+02:00",
                ],
            ),
            weather=WeatherInfoDTO(
                temp=13.92,
                pressure=1023,
                humidity=54,
                wind_speed=4.63,
                description="scattered clouds",
                visibility=10000,
                timezone=3600,
                date_time=2023-03-30 12:23:34
            ),
            currency_rates={
                "EUR": 0.016503,
            },
            news=[
                NewsDTO(
                   title="Maia Sandu: Republica Moldova este ținta unor atacuri hibride finanțate de Kremlin. i",
                   author="Ion Gaidău",
                   description="Preşedinta Maia Sandu a avertizat că Republica Moldova este ținta unor atacuri hidride",
                   source="Adevarul.ro",
                   url="https://adevarul.ro/stiri-externe/republica-moldova/maia-sandu-republica-moldova-este-tinta-
                   unor-2254533.html"
                   published_at=2023-03-30T12:42:34Z,
                )
            ]
        )
    """

    location: CountryDTO
    weather: WeatherInfoDTO
    currency_rates: dict[str, float]
    news: Optional[list[NewsDTO]]
