import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stock_table import (
    stock_table,
    skeleton_loader,
    empty_state,
    stock_row,
)
from app.components.add_stock_dialog import add_stock_dialog
from app.states.stock_state import StockState
from app.states.watchlist_state import WatchlistState
from app.components.metric_cards import metric_card, metric_cards


def page_layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(content, add_stock_dialog(), class_name="p-6"),
            on_mount=StockState.fetch_stocks,
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name="flex bg-[#0a0f1a] text-slate-200 font-['Inter']",
    )


def index() -> rx.Component:
    return page_layout(
        rx.el.div(
            metric_cards(),
            rx.el.div(
                rx.cond(
                    StockState.is_loading,
                    rx.el.div(
                        skeleton_loader(),
                        skeleton_loader(),
                        skeleton_loader(),
                        skeleton_loader(),
                        class_name="bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
                    ),
                    rx.cond(
                        StockState.error_message,
                        rx.el.div(
                            rx.icon(
                                "flag_triangle_right",
                                class_name="h-10 w-10 text-yellow-500 mb-4",
                            ),
                            rx.el.p(
                                "An error occurred",
                                class_name="font-bold text-lg text-slate-300",
                            ),
                            rx.el.p(
                                StockState.error_message,
                                class_name="text-sm text-slate-500",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 bg-yellow-900/20 rounded-lg border border-yellow-700/50",
                        ),
                        rx.cond(
                            StockState.stocks.length() > 0, stock_table(), empty_state()
                        ),
                    ),
                ),
                class_name="mt-6",
            ),
        ),
        title="Dashboard",
    )


def watchlist() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                metric_card(
                    "Watchlist Stocks",
                    WatchlistState.total_watchlist_stocks.to_string(),
                    "star",
                    "text-yellow-400",
                    "border-yellow-500",
                ),
                metric_card(
                    "Avg. Change",
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        f"+{WatchlistState.average_watchlist_change.to_string()}",
                        WatchlistState.average_watchlist_change.to_string(),
                    ),
                    "trending-up",
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        "text-green-400",
                        "text-red-400",
                    ),
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        "border-green-500",
                        "border-red-500",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.cond(
                    WatchlistState.is_loading,
                    rx.el.div(
                        skeleton_loader(),
                        skeleton_loader(),
                        class_name="bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
                    ),
                    rx.cond(
                        WatchlistState.watchlist_stocks.length() > 0,
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
                            rx.el.tbody(
                                rx.foreach(WatchlistState.watchlist_stocks, stock_row)
                            ),
                            class_name="w-full",
                        ),
                        empty_state(),
                    ),
                ),
                class_name="mt-6 bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
            ),
        ),
        title="Watchlist",
    )


def settings() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-xl font-bold text-slate-100 mb-6"),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "User Preferences",
                        class_name="text-lg font-semibold text-slate-200 mb-4 border-b border-slate-700 pb-2",
                    ),
                    rx.el.p(
                        "Theme and notification settings will be here.",
                        class_name="text-slate-400",
                    ),
                    class_name="bg-[#151b28] p-6 rounded-lg border border-slate-800 mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Data Management",
                        class_name="text-lg font-semibold text-slate-200 mb-4 border-b border-slate-700 pb-2",
                    ),
                    rx.el.p(
                        "Data export and clear options will be here.",
                        class_name="text-slate-400",
                    ),
                    class_name="bg-[#151b28] p-6 rounded-lg border border-slate-800 mb-6",
                ),
                rx.el.div(
                    rx.el.h3(
                        "About",
                        class_name="text-lg font-semibold text-slate-200 mb-4 border-b border-slate-700 pb-2",
                    ),
                    rx.el.p("StockDash v1.0.0", class_name="text-slate-400"),
                    class_name="bg-[#151b28] p-6 rounded-lg border border-slate-800",
                ),
            ),
        ),
        title="Settings",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(watchlist)
app.add_page(settings)