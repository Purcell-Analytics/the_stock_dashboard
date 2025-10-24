import reflex as rx
from app.states.stock_state import StockState
from app.util.supabase_client import get_supabase_client
import logging
import json
import csv
from datetime import datetime


class DataState(StockState):
    show_clear_stocks_dialog: bool = False

    @rx.var
    def total_records(self) -> int:
        return self.total_stocks

    @rx.var
    def last_updated(self) -> str:
        if not self.stocks:
            return "N/A"
        latest_stock = max(self.stocks, key=lambda s: s.get("last_updated", ""))
        if not latest_stock or not latest_stock.get("last_updated"):
            return "N/A"
        dt_object = datetime.fromisoformat(
            latest_stock["last_updated"].replace("Z", "+00:00")
        )
        return dt_object.strftime("%Y-%m-%d %H:%M:%S")

    @rx.event
    def export_data(self, file_type: str):
        all_stocks = self.stocks
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"stock_export_{timestamp}.{file_type}"
        if file_type == "json":
            content = json.dumps(all_stocks, indent=2)
            return rx.download(data=content, filename=filename)
        if file_type == "csv":
            if not all_stocks:
                return rx.toast("No data to export.", duration=3000)
            output = [list(all_stocks[0].keys())] + [
                list(stock.values()) for stock in all_stocks
            ]
            csv_content = """
""".join([",".join(map(str, row)) for row in output])
            return rx.download(data=csv_content, filename=filename)

    @rx.event(background=True)
    async def clear_watchlist(self):
        async with self:
            self.is_loading = True
        try:
            client = get_supabase_client()
            if not client:
                async with self:
                    self.error_message = "Supabase client not available."
                    self.is_loading = False
                return
            client.table("stocks").update({"is_watchlist": False}).neq(
                "is_watchlist", False
            ).execute()
            yield rx.toast("Watchlist cleared successfully.", duration=3000)
            yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error clearing watchlist: {e}")
            async with self:
                self.error_message = f"Failed to clear watchlist: {e}"
                self.is_loading = False
                yield rx.toast(self.error_message, duration=5000)

    @rx.event(background=True)
    async def clear_all_stocks(self):
        async with self:
            self.is_loading = True
        try:
            client = get_supabase_client()
            if not client:
                async with self:
                    self.error_message = "Supabase client not available."
                    self.is_loading = False
                return
            client.table("stocks").delete().neq("id", -1).execute()
            yield rx.toast("All stocks have been deleted.", duration=3000)
            yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error deleting all stocks: {e}")
            async with self:
                self.error_message = f"Failed to delete all stocks: {e}"
                self.is_loading = False
                yield rx.toast(self.error_message, duration=5000)