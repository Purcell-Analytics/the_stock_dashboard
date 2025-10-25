import reflex as rx
from app.states.stock_state import Stock, StockState
from app.states.watchlist_state import WatchlistState
from app.states.settings_state import SettingsState


def stock_row(stock: Stock) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(stock["symbol"], class_name="font-bold text-slate-100"),
                rx.el.p(stock["name"], class_name="text-slate-400 text-xs"),
                class_name="pl-6 py-3",
            )
        ),
        rx.el.td(
            f"{SettingsState.currency_symbol}{stock['price'].to_string()}",
            class_name="text-sm font-medium text-slate-200 text-right",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    stock["change"] >= 0,
                    f"+{stock['change'].to_string()}",
                    stock["change"].to_string(),
                ),
                class_name=rx.cond(
                    stock["change"] >= 0, "text-green-400", "text-red-400"
                ),
            ),
            class_name="text-sm font-medium text-right",
        ),
        rx.el.td(
            stock["volume"].to_string(), class_name="text-sm text-slate-300 text-right"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "star",
                        class_name=rx.cond(
                            stock["is_watchlist"],
                            "h-4 w-4 text-yellow-400 fill-yellow-400",
                            "h-4 w-4",
                        ),
                    ),
                    on_click=lambda: StockState.toggle_watchlist(
                        stock["id"], stock["is_watchlist"]
                    ),
                    class_name="text-slate-500 hover:text-yellow-400 p-2 rounded-md",
                ),
                rx.el.a(
                    rx.icon("bar-chart-2", class_name="h-4 w-4"),
                    href=f"/stock/{stock['symbol']}",
                    class_name="text-slate-500 hover:text-cyan-400 p-2 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: StockState.delete_stock(stock["id"]),
                    class_name="text-slate-500 hover:text-red-400 p-2 rounded-md",
                    disabled=StockState.is_deleting,
                ),
                class_name="flex justify-end",
            ),
            class_name="pr-6 py-3 text-right",
        ),
        class_name="border-b border-slate-800 hover:bg-slate-800/50 transition-colors",
    )


def stock_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Stock",
                        class_name="text-left font-semibold text-slate-400 uppercase text-xs tracking-wider pl-6 py-3",
                    ),
                    rx.el.th(
                        "Price",
                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th(
                        "Change",
                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th(
                        "Volume",
                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th("", class_name="pr-6 py-3"),
                    class_name="bg-slate-800/50",
                )
            ),
            rx.el.tbody(rx.foreach(StockState.filtered_stocks, stock_row)),
            class_name="w-full",
        ),
        class_name="bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
    )


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-4 bg-slate-700 rounded w-1/4"),
            rx.el.div(class_name="h-3 bg-slate-700 rounded w-1/2 mt-1"),
            class_name="pl-6 py-3",
        ),
        class_name="animate-pulse flex items-center h-16 border-b border-slate-800",
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.icon("inbox", class_name="h-12 w-12 text-slate-500"),
        rx.el.h3(
            "No stocks found", class_name="mt-4 text-lg font-semibold text-slate-200"
        ),
        rx.el.p(
            "Add a new stock to get started.", class_name="mt-1 text-sm text-slate-400"
        ),
        class_name="flex flex-col items-center justify-center text-center p-12 bg-[#151b28] rounded-lg border border-slate-800",
    )