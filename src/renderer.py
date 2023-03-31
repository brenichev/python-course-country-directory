"""
Функции для формирования выходной информации.
"""

from decimal import ROUND_HALF_UP, Decimal

from prettytable import PrettyTable

from collectors.models import LocationInfoDTO


class Renderer:
    """
    Генерация результата преобразования прочитанных данных.
    """

    def __init__(self, location_info: LocationInfoDTO) -> None:
        """
        Конструктор.

        :param location_info: Данные о географическом месте.
        """

        self.location_info = location_info

    async def render(self) -> tuple[str, ...]:
        """
        Форматирование прочитанных данных.

        :return: Результат форматирования
        """

        info_table = PrettyTable()

        info_table.field_names = [
            "Страна",
            "Столица",
            "Широта",
            "Долгота",
            "Регион",
            "Население страны",
            "Языки",
            "Площадь",
            "Часовой пояс",
            "Курсы валют",
        ]

        info_table.add_row(
            [
                self.location_info.location.name,
                self.location_info.location.capital,
                self.location_info.location.capital_latitude,
                self.location_info.location.capital_longitude,
                self.location_info.location.subregion,
                f"{await self._format_population()} чел.",
                await self._format_languages(),
                f"{self.location_info.location.capital_area} кв. км.",
                self.location_info.location.timezones[0],
                await self._format_currency_rates(),
            ]
        )

        weather_table = PrettyTable()
        weather_table.field_names = [
            "Температура",
            "Описание",
            "Видимость",
            "Скорость ветра",
            "Время получения данных",
        ]
        weather_table.add_row(
            [
                f"{self.location_info.weather.temp} °C",
                self.location_info.weather.description,
                f"{self.location_info.weather.visibility} м.",
                f"{self.location_info.weather.wind_speed} м/с.",
                self.location_info.weather.date_time.strftime("%d.%m.%Y %H:%M"),
            ]
        )

        news_table = PrettyTable(
            border=True, preserve_internal_border=True, padding_width=5
        )

        news_table.field_names = [
            "Источник",
            "Название",
            "Автор",
            "Ссылка",
            "Описание",
            "Дата публикации",
        ]

        # pylint: disable=W0212
        news_table._max_width = {"Название": 25, "Ссылка": 25, "Описание": 45}

        for article in self.location_info.news:  # type: ignore[union-attr]
            news_table.add_row(
                [
                    f"{article.source}",
                    f"{article.title}",
                    f"{article.author}",
                    article.url,
                    f"{article.description}",
                    article.published_at.strftime("%d.%m.%Y %H:%M"),
                ]
            )

        return (
            info_table,
            "Погода:",
            weather_table,
            "Новости",
            news_table,
        )  # type: ignore[return-value]

    async def _format_languages(self) -> str:
        """
        Форматирование информации о языках.

        :return:
        """

        return ", ".join(
            f"{item.name} ({item.native_name})"
            for item in self.location_info.location.languages
        )

    async def _format_population(self) -> str:
        """
        Форматирование информации о населении.

        :return:
        """

        # pylint: disable=C0209
        return "{:,}".format(self.location_info.location.population).replace(",", ".")

    async def _format_currency_rates(self) -> str:
        """
        Форматирование информации о курсах валют.

        :return:
        """

        return ", ".join(
            f"{currency} = {Decimal(rates).quantize(exp=Decimal('.01'), rounding=ROUND_HALF_UP)} руб."
            for currency, rates in self.location_info.currency_rates.items()
        )
