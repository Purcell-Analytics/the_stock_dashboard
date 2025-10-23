import reflex as rx
from app.states.stock_state import Stock, StockState


def stock_row(stock: Stock) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(stock["symbol"], class_name="font-bold text-gray-900"),
                rx.el.p(stock["name"], class_name="text-gray-500 text-xs"),
                class_name="pl-6 py-3",
            )
        ),
        rx.el.td(
            f"${stock['price'].to_string()}",
            class_name="text-sm font-medium text-gray-800 text-right",
        ),
        rx.el.td(
            rx.el.span(
                rx.cond(
                    stock["change"] >= 0,
                    f"+{stock['change'].to_string()}",
                    stock["change"].to_string(),
                ),
                class_name=rx.cond(
                    stock["change"] >= 0, "text-green-600", "text-red-600"
                ),
            ),
            class_name="text-sm font-medium text-right",
        ),
        rx.el.td(
            stock["volume"].to_string(), class_name="text-sm text-gray-600 text-right"
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("trash-2", class_name="h-4 w-4"),
                on_click=lambda: StockState.delete_stock(stock["id"]),
                class_name="text-gray-400 hover:text-red-600 p-2 rounded-md",
            ),
            class_name="pr-6 py-3 text-right",
        ),
        class_name="border-b border-gray-200 hover:bg-gray-50/50 transition-colors",
    )


def stock_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Stock",
                        class_name="text-left font-semibold text-gray-600 uppercase text-xs tracking-wider pl-6 py-3",
                    ),
                    rx.el.th(
                        "Price",
                        class_name="text-right font-semibold text-gray-600 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th(
                        "Change",
                        class_name="text-right font-semibold text-gray-600 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th(
                        "Volume",
                        class_name="text-right font-semibold text-gray-600 uppercase text-xs tracking-wider",
                    ),
                    rx.el.th("", class_name="pr-6 py-3"),
                    class_name="bg-gray-50",
                )
            ),
            rx.el.tbody(rx.foreach(StockState.filtered_stocks, stock_row)),
            class_name="w-full",
        ),
        class_name="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-[0px_1px_3px_rgba(0,0,0,0.12)]",
    )


def skeleton_loader() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-4 bg-gray-200 rounded w-1/4"),
            rx.el.div(class_name="h-3 bg-gray-200 rounded w-1/2 mt-1"),
            class_name="pl-6 py-3",
        ),
        class_name="animate-pulse flex items-center h-16 border-b border-gray-200",
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.icon("inbox", class_name="h-12 w-12 text-gray-400"),
        rx.el.h3(
            "No stocks found", class_name="mt-4 text-lg font-semibold text-gray-800"
        ),
        rx.el.p(
            "Add a new stock to get started.", class_name="mt-1 text-sm text-gray-500"
        ),
        class_name="flex flex-col items-center justify-center text-center p-12 bg-white rounded-lg border border-gray-200 shadow-sm",
    )