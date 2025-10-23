import reflex as rx
from app.states.stock_state import StockState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-2xl font-bold text-gray-800"),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                    rx.el.input(
                        placeholder="Search stocks...",
                        on_change=StockState.set_search_query,
                        class_name="bg-transparent focus:outline-none w-full text-sm font-medium text-gray-800 placeholder-gray-500",
                    ),
                    class_name="flex items-center gap-3 bg-gray-100/75 border border-gray-200/50 rounded-lg px-3 py-2 w-64",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2 h-4 w-4"),
                    "Add Stock",
                    on_click=StockState.toggle_add_stock_dialog,
                    class_name="flex items-center bg-violet-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-violet-700 transition-colors duration-200 shadow-[0px_1px_3px_rgba(0,0,0,0.12)]",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white/80 backdrop-blur-sm sticky top-0 z-10 h-16 border-b px-6",
    )