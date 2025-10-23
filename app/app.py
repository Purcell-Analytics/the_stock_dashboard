import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stock_table import stock_table, skeleton_loader, empty_state
from app.components.add_stock_dialog import add_stock_dialog
from app.states.stock_state import StockState
from app.components.metric_cards import metric_cards


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(
                metric_cards(),
                rx.el.div(
                    rx.cond(
                        StockState.is_loading,
                        rx.el.div(
                            skeleton_loader(),
                            skeleton_loader(),
                            skeleton_loader(),
                            skeleton_loader(),
                            class_name="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-[0px_1px_3px_rgba(0,0,0,0.12)]",
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
                                    class_name="font-bold text-lg text-gray-700",
                                ),
                                rx.el.p(
                                    StockState.error_message,
                                    class_name="text-sm text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center p-8 bg-yellow-50 rounded-lg border border-yellow-200",
                            ),
                            rx.cond(
                                StockState.stocks.length() > 0,
                                stock_table(),
                                empty_state(),
                            ),
                        ),
                    ),
                    class_name="mt-6",
                ),
                add_stock_dialog(),
                class_name="p-6",
            ),
            on_mount=StockState.fetch_stocks,
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name="flex bg-gray-50 font-['Inter']",
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