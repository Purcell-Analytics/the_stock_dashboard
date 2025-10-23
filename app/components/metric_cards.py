import reflex as rx
from app.states.stock_state import StockState


def metric_card(title: str, value: rx.Var, icon_name: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-800"),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-lg border border-gray-200 shadow-sm",
    )


def biggest_gainer_card() -> rx.Component:
    return rx.el.div(
        rx.cond(
            StockState.biggest_gainer,
            rx.el.div(
                rx.el.div(
                    rx.icon("trending-up", class_name="h-6 w-6 text-green-600"),
                    class_name="p-3 bg-gray-100 rounded-lg",
                ),
                rx.el.div(
                    rx.el.p(
                        "Biggest Gainer", class_name="text-sm font-medium text-gray-500"
                    ),
                    rx.el.div(
                        rx.el.p(
                            StockState.biggest_gainer["symbol"],
                            class_name="text-xl font-semibold text-gray-800",
                        ),
                        rx.el.p(
                            f"+{StockState.biggest_gainer['change'].to_string()}",
                            class_name="text-sm font-medium text-green-600",
                        ),
                        class_name="flex items-baseline gap-2",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex items-center gap-4 p-4 bg-white rounded-lg border border-gray-200 shadow-sm",
            ),
            metric_card("Biggest Gainer", "N/A", "trending-up", "text-gray-500"),
        )
    )


def metric_cards() -> rx.Component:
    return rx.el.div(
        metric_card("Total Stocks", StockState.total_stocks, "binary", "text-blue-600"),
        metric_card(
            "Average Price",
            f"${StockState.average_price.to_string()}",
            "dollar-sign",
            "text-yellow-600",
        ),
        metric_card(
            "Total Volume",
            StockState.total_volume.to_string(),
            "bar-chart-3",
            "text-purple-600",
        ),
        biggest_gainer_card(),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
    )