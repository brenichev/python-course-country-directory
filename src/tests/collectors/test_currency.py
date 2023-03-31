"""
Тестирование функций сбора информации о курсах валют.
"""
import json

import aiofiles
import pytest

from collectors.collector import CurrencyRatesCollector


@pytest.mark.asyncio
class TestCollectorCurrency:
    @pytest.fixture(autouse=True)
    def collector(self):
        return CurrencyRatesCollector()

    @pytest.mark.asyncio
    async def test_read_currencies(self, collector):
        """
        Тестирование чтения информации о валютах.
        """
        currencies = await collector.read()
        assert currencies is not None
        assert currencies.base.lower() == "rub"
        assert len(currencies.rates) == 170

    @pytest.mark.asyncio
    async def test_collecting_currencies(self, collector):
        """
        Тестирование получения информации о валютах.
        """
        await collector.collect()
        async with aiofiles.open(await collector.get_file_path(), mode="r") as file:
            json_currencies = json.loads(await file.read())
        read_currencies = await collector.read()
        assert json_currencies["base"] == read_currencies.base
        assert len(json_currencies["rates"]) == len(read_currencies.rates)
