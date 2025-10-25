import reflex as rx
from typing import Literal
from datetime import datetime, timedelta
import logging
import os
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

Timeframe = Literal["1D", "1W", "1M", "3M", "6M", "1Y", "ALL"]


class ChartState(rx.State):
    chart_data: list[dict[str, float | str]] = []
    selected_symbol: str = ""
    selected_timeframe: Timeframe = "1Y"
    is_loading_chart: bool = False
    chart_error_message: str = ""
    _data_cache: dict[str, dict] = {}

    @rx.event(background=True)
    async def fetch_chart_data(self, symbol: str):
        async with self:
            if not symbol:
                return
            self.is_loading_chart = True
            self.selected_symbol = symbol
            self.chart_error_message = ""
            self.chart_data = []
            now = datetime.now()
            if (
                symbol in self._data_cache
                and self.selected_timeframe in self._data_cache[symbol]
            ):
                cache_entry = self._data_cache[symbol][self.selected_timeframe]
                if now - cache_entry["last_fetch"] < timedelta(minutes=5):
                    self.chart_data = cache_entry["data"]
                    self.is_loading_chart = False
                    return
        try:
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                async with self:
                    self.chart_error_message = "Alpha Vantage API key not configured."
                    yield rx.toast(self.chart_error_message, duration=5000)
                return
            ts = TimeSeries(key=api_key, output_format="pandas")
            output_size = (
                "full" if self.selected_timeframe in ["1Y", "ALL"] else "compact"
            )
            data: pd.DataFrame
            meta_data: dict
            data, meta_data = ts.get_daily(symbol=symbol, outputsize=output_size)
            end_date = data.index.max()
            if self.selected_timeframe == "1D":
                start_date = end_date - timedelta(days=1)
            elif self.selected_timeframe == "1W":
                start_date = end_date - timedelta(weeks=1)
            elif self.selected_timeframe == "1M":
                start_date = end_date - timedelta(days=30)
            elif self.selected_timeframe == "3M":
                start_date = end_date - timedelta(days=90)
            elif self.selected_timeframe == "6M":
                start_date = end_date - timedelta(days=180)
            elif self.selected_timeframe == "1Y":
                start_date = end_date - timedelta(days=365)
            else:
                start_date = data.index.min()
            filtered_data = data[data.index >= start_date]
            formatted_data = []
            for index, row in filtered_data.iterrows():
                formatted_data.append(
                    {
                        "date": index.strftime("%Y-%m-%d"),
                        "open": row["1. open"],
                        "high": row["2. high"],
                        "low": row["3. low"],
                        "close": row["4. close"],
                        "volume": row["5. volume"],
                    }
                )
            async with self:
                self.chart_data = formatted_data[::-1]
                if symbol not in self._data_cache:
                    self._data_cache[symbol] = {}
                self._data_cache[symbol][self.selected_timeframe] = {
                    "data": self.chart_data,
                    "last_fetch": now,
                }
        except Exception as e:
            logging.exception(f"Error fetching chart data for {symbol}: {e}")
            async with self:
                error_str = str(e)
                if "call frequency" in error_str.lower():
                    self.chart_error_message = (
                        "API rate limit exceeded. Please try again later."
                    )
                else:
                    self.chart_error_message = f"Could not fetch data for {symbol}."
                yield rx.toast(self.chart_error_message, duration=5000)
        finally:
            async with self:
                self.is_loading_chart = False

    @rx.event
    def set_timeframe(self, timeframe: Timeframe):
        self.selected_timeframe = timeframe
        if self.selected_symbol:
            return ChartState.fetch_chart_data(self.selected_symbol)

    @rx.event(background=True)
    async def on_load_chart(self):
        symbol = self.router.page.params.get("symbol", "")
        if symbol:
            async with self:
                self.selected_symbol = symbol.upper()
            yield ChartState.fetch_chart_data(self.selected_symbol)