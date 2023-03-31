"""
Тестирование функций сбора информации о новостях.
"""
import pytest
from collectors.collector import NewsCollector
from collectors.models import LocationDTO


class TestCollectorNews:
    """
    Тестирование функций сбора информации о новостях.
    """

    @pytest.fixture(autouse=True)
    def collector(self):
        return NewsCollector()

    @pytest.fixture(autouse=True)
    def location(self):
        return LocationDTO(capital="Moscow", alpha2code="RU")

    @pytest.fixture(autouse=True)
    def number(self):
        return 2

    @pytest.mark.asyncio
    async def test_read_news(self, collector, location, number):
        """
        Тестирование чтения информации о новостях.
        """
        weather = await collector.read(location, number)
        assert weather is not None

    @pytest.mark.asyncio
    async def test_collect_news(self, collector, location):
        """
        Тестирование получения информации о новостях.
        """
        await collector.collect(frozenset([location]))
