import reflex as rx
from app.states.stock_state import StockState
from app.util.supabase_client import get_supabase_client
import logging
import yfinance as yf
from datetime import datetime, timezone


class ApiState(StockState):
    is_syncing: bool = False
    last_sync_time: str = rx.LocalStorage("", name="last_sync_time")
    sync_success_count: int = 0
    sync_error_count: int = 0

    @rx.event(background=True)
    async def sync_all_stocks(self):
        async with self:
            if self.is_syncing:
                return
            self.is_syncing = True
            self.sync_success_count = 0
            self.sync_error_count = 0
        all_stocks = self.stocks
        if not all_stocks:
            async with self:
                self.is_syncing = False
            return
        symbols = [stock["symbol"] for stock in all_stocks]
        try:
            data = yf.download(tickers=symbols, period="1d", group_by="ticker")
            updates = []
            for stock in all_stocks:
                symbol = stock["symbol"]
                try:
                    stock_data = data[symbol]
                    if not stock_data.empty:
                        latest = stock_data.iloc[-1]
                        price = float(latest["Close"])
                        prev_close = float(latest["Open"])
                        change = price - prev_close
                        volume = int(latest["Volume"])
                        updates.append(
                            {
                                "id": stock["id"],
                                "price": round(price, 2),
                                "change": round(change, 2),
                                "volume": volume,
                            }
                        )
                        async with self:
                            self.sync_success_count += 1
                    else:
                        async with self:
                            self.sync_error_count += 1
                except Exception as e:
                    logging.exception(f"Error processing stock {symbol}: {e}")
                    async with self:
                        self.sync_error_count += 1
            if updates:
                client = get_supabase_client()
                if client:
                    client.table("stocks").upsert(updates).execute()
            async with self:
                self.last_sync_time = datetime.now(timezone.utc).isoformat()
            yield rx.toast(
                f"Sync complete: {self.sync_success_count} updated, {self.sync_error_count} failed.",
                duration=3000,
            )
            yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error syncing all stocks: {e}")
            yield rx.toast(f"API Sync Error: {e}", duration=5000)
        finally:
            async with self:
                self.is_syncing = False

    @rx.event(background=True)
    async def sync_single_stock(self, symbol: str):
        async with self:
            self.is_syncing = True
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            prev_close = info.get("previousClose", 0)
            change = price - prev_close if price and prev_close else 0
            volume = info.get("volume", info.get("regularMarketVolume", 0))
            stock_to_update = next(
                (s for s in self.stocks if s["symbol"] == symbol), None
            )
            if stock_to_update:
                client = get_supabase_client()
                if client:
                    client.table("stocks").update(
                        {
                            "price": round(price, 2),
                            "change": round(change, 2),
                            "volume": volume,
                        }
                    ).eq("id", stock_to_update["id"]).execute()
                    yield rx.toast(f"Synced {symbol} successfully.", duration=3000)
                    yield StockState.fetch_stocks
        except Exception as e:
            logging.exception(f"Error syncing single stock: {e}")
            yield rx.toast(f"Failed to sync {symbol}: {e}", duration=5000)
        finally:
            async with self:
                self.is_syncing = False