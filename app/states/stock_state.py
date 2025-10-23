import reflex as rx
from typing import TypedDict, Optional
from app.util.supabase_client import get_supabase_client
import logging


class Stock(TypedDict):
    id: int
    symbol: str
    name: str
    price: float
    change: float
    volume: int
    last_updated: str


class StockState(rx.State):
    stocks: list[Stock] = []
    is_loading: bool = True
    error_message: str = ""
    form_symbol: str = ""
    form_name: str = ""
    form_price: str = ""
    form_change: str = ""
    form_volume: str = ""
    show_add_stock_dialog: bool = False
    search_query: str = ""

    @rx.var
    def filtered_stocks(self) -> list[Stock]:
        if not self.search_query:
            return self.stocks
        return [
            stock
            for stock in self.stocks
            if self.search_query.lower() in stock["symbol"].lower()
            or self.search_query.lower() in stock["name"].lower()
        ]

    @rx.var
    def total_stocks(self) -> int:
        return len(self.stocks)

    @rx.var
    def average_price(self) -> float:
        if not self.stocks:
            return 0.0
        total_price = sum((stock["price"] for stock in self.stocks))
        return round(total_price / len(self.stocks), 2)

    @rx.var
    def total_volume(self) -> int:
        return sum((stock["volume"] for stock in self.stocks))

    @rx.var
    def biggest_gainer(self) -> Stock | None:
        if not self.stocks:
            return None
        return max(self.stocks, key=lambda s: s.get("change", 0))

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def toggle_add_stock_dialog(self):
        self.show_add_stock_dialog = not self.show_add_stock_dialog
        self.form_symbol = ""
        self.form_name = ""
        self.form_price = ""
        self.form_change = ""
        self.form_volume = ""
        self.error_message = ""

    @rx.event(background=True)
    async def fetch_stocks(self):
        async with self:
            self.is_loading = True
            self.error_message = ""
        try:
            client = get_supabase_client()
            if not client:
                async with self:
                    self.error_message = "Supabase client not available."
                    self.is_loading = False
                return
            response = client.table("stocks").select("*").order("symbol").execute()
            async with self:
                if response.data:
                    self.stocks = response.data
                else:
                    self.stocks = []
                self.is_loading = False
        except Exception as e:
            logging.exception(f"Error fetching stocks: {e}")
            async with self:
                self.error_message = f"Failed to fetch stocks: {e}"
                self.is_loading = False
                yield rx.toast(self.error_message, duration=5000)

    @rx.event(background=True)
    async def add_stock(self, form_data: dict):
        async with self:
            self.is_loading = True
        try:
            symbol = form_data.get("symbol", "").upper()
            name = form_data.get("name", "")
            price = float(form_data.get("price", 0))
            change = float(form_data.get("change", 0))
            volume = int(form_data.get("volume", 0))
            if not all([symbol, name]):
                async with self:
                    self.error_message = "Symbol and Name are required."
                    yield rx.toast(self.error_message, duration=4000)
                    self.is_loading = False
                return
            client = get_supabase_client()
            if not client:
                async with self:
                    self.error_message = "Supabase client not available."
                    self.is_loading = False
                return
            client.table("stocks").insert(
                {
                    "symbol": symbol,
                    "name": name,
                    "price": price,
                    "change": change,
                    "volume": volume,
                }
            ).execute()
            async with self:
                self.show_add_stock_dialog = False
            yield rx.toast(f"Successfully added {symbol}.", duration=3000)
            yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error adding stock: {e}")
            async with self:
                self.error_message = f"Failed to add stock: {e}"
                self.is_loading = False
                yield rx.toast(self.error_message, duration=5000)

    @rx.event(background=True)
    async def delete_stock(self, stock_id: int):
        async with self:
            self.is_loading = True
        try:
            client = get_supabase_client()
            if not client:
                async with self:
                    self.error_message = "Supabase client not available."
                    self.is_loading = False
                return
            client.table("stocks").delete().eq("id", stock_id).execute()
            yield rx.toast("Stock deleted successfully.", duration=3000)
            yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error deleting stock: {e}")
            async with self:
                self.error_message = f"Failed to delete stock: {e}"
                self.is_loading = False
                yield rx.toast(self.error_message, duration=5000)