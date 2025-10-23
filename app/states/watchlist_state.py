import reflex as rx
from app.states.stock_state import StockState, Stock


class WatchlistState(StockState):
    @rx.var
    def watchlist_stocks(self) -> list[Stock]:
        return [stock for stock in self.stocks if stock.get("is_watchlist")]

    @rx.var
    def total_watchlist_stocks(self) -> int:
        return len(self.watchlist_stocks)

    @rx.var
    def average_watchlist_change(self) -> float:
        if not self.watchlist_stocks:
            return 0.0
        total_change = sum((stock["change"] for stock in self.watchlist_stocks))
        return round(total_change / len(self.watchlist_stocks), 2)