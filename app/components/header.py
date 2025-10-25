import reflex as rx
from app.states.stock_state import StockState
from app.states.api_state import ApiState


def header(title: str) -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1(title, class_name="text-2xl font-bold text-slate-100"),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-slate-500"),
                    rx.el.input(
                        placeholder="Search stocks...",
                        on_change=StockState.set_search_query,
                        class_name="bg-transparent focus:outline-none w-full text-sm font-medium text-slate-100 placeholder-slate-500",
                    ),
                    class_name="flex items-center gap-3 bg-slate-800/50 border border-slate-700 rounded-lg px-3 py-2 w-64",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            ApiState.is_syncing,
                            rx.spinner(class_name="h-4 w-4"),
                            rx.icon("refresh-cw", class_name="h-4 w-4"),
                        ),
                        "Sync All",
                        on_click=ApiState.sync_all_stocks,
                        disabled=ApiState.is_syncing,
                        class_name="flex items-center gap-2 bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-slate-600 transition-colors duration-200 disabled:opacity-50",
                    ),
                    rx.el.p(
                        f"Last sync: {ApiState.last_sync_time}",
                        class_name="text-xs text-slate-500 mt-1",
                    ),
                    class_name="flex flex-col items-center",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Stock",
                    on_click=StockState.toggle_add_stock_dialog,
                    class_name="flex items-center bg-cyan-500 text-slate-900 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-cyan-600 transition-colors duration-200",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-[#151b28]/80 backdrop-blur-sm sticky top-0 z-10 h-16 border-b border-slate-800 px-6",
    )