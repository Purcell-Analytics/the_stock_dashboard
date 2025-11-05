import reflex as rx
import logging
import os
from typing import TypedDict
import httpx
from app.states.stock_state import StockState
from app.util.supabase_client import get_supabase_client


class AvailableStock(TypedDict):
    symbol: str
    name: str
    exchange: str


class ImportState(rx.State):
    show_dialog: bool = False
    available_stocks: list[AvailableStock] = []
    selected_stocks: set[str] = set()
    is_loading: bool = False
    is_importing: bool = False
    search_query: str = ""

    @rx.event
    def toggle_dialog(self):
        self.show_dialog = not self.show_dialog
        if self.show_dialog and (not self.available_stocks):
            return ImportState.fetch_available_stocks

    @rx.event(background=True)
    async def fetch_available_stocks(self):
        async with self:
            if self.is_loading or self.available_stocks:
                return
            self.is_loading = True
        try:
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not api_key:
                yield rx.toast("API key is not configured.", duration=5000)
                return
            url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                lines = response.text.strip().split("""\r
""")
                stocks = []
                for line in lines[1:]:
                    parts = line.split(",")
                    if (
                        len(parts) >= 7
                        and parts[3].lower() == "stock"
                        and (parts[6].lower() == "active")
                    ):
                        stocks.append(
                            {"symbol": parts[0], "name": parts[1], "exchange": parts[2]}
                        )
                async with self:
                    self.available_stocks = stocks
        except Exception as e:
            logging.exception(f"Error fetching available stocks: {e}")
            yield rx.toast("Failed to fetch available stocks.", duration=5000)
        finally:
            async with self:
                self.is_loading = False

    @rx.event
    def toggle_stock_selection(self, symbol: str):
        if symbol in self.selected_stocks:
            self.selected_stocks.remove(symbol)
        else:
            self.selected_stocks.add(symbol)

    @rx.var
    def filtered_available_stocks(self) -> list[AvailableStock]:
        if not self.search_query:
            return self.available_stocks[:100]
        query = self.search_query.lower()
        return [
            s
            for s in self.available_stocks
            if query in s["symbol"].lower() or query in s["name"].lower()
        ][:100]

    @rx.event(background=True)
    async def import_selected_stocks(self):
        async with self:
            if not self.selected_stocks or self.is_importing:
                return
            self.is_importing = True
        stocks_to_insert = []
        for symbol in self.selected_stocks:
            stock_info = next(
                (s for s in self.available_stocks if s["symbol"] == symbol), None
            )
            if stock_info:
                stocks_to_insert.append(
                    {
                        "symbol": stock_info["symbol"],
                        "name": stock_info["name"],
                        "price": 0,
                        "change": 0,
                        "volume": 0,
                    }
                )
        try:
            client = get_supabase_client()
            if not client:
                yield rx.toast("Database connection not available.", duration=5000)
                return
            client.table("stocks").upsert(
                stocks_to_insert, on_conflict="symbol"
            ).execute()
            yield rx.toast(
                f"Successfully imported {len(stocks_to_insert)} stocks.", duration=3000
            )
            async with self:
                self.selected_stocks.clear()
                self.show_dialog = False
            yield StockState.fetch_stocks(True)
        except Exception as e:
            logging.exception(f"Error importing stocks: {e}")
            yield rx.toast("Failed to import stocks.", duration=5000)
        finally:
            async with self:
                self.is_importing = False