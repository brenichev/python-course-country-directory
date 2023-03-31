"""
Тестирование функций клиента для получения информации о погоде.
"""
import pytest
from collectors.collector import WeatherCollector
from collectors.models import LocationDTO


class TestClientWeather:
    """
    Тестирование функций сбора информации о погоде.
    """

    @pytest.fixture(autouse=True)
    def collector(self):
        return WeatherCollector()

    @pytest.fixture(autouse=True)
    def location(self):
        return LocationDTO(
            capital="Moscow",
            alpha2code="RU",
        )

    @pytest.mark.asyncio
    async def test_read_weather(self, location, collector):
        """
        Тестирование чтения информации о погоде.
        """
        weather = await collector.read(location)
        assert weather is not None

    @pytest.mark.asyncio
    async def test_collect_weather(self, location, collector):
        """
        Тестирование получения информации о погоде.
        """
        w = await collector.collect(frozenset([location]))
        assert w is None
