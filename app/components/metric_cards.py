import reflex as rx
from app.states.stock_state import StockState
from app.states.settings_state import SettingsState


def metric_card(
    title: str, value: rx.Var, icon_name: str, icon_color: str, border_color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=icon_color),
            class_name="p-3 bg-slate-800 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-slate-400"),
            rx.el.p(value, class_name="text-2xl font-semibold text-slate-100"),
            class_name="flex-1",
        ),
        class_name="flex items-center gap-4 p-5 bg-[#151b28] rounded-lg border-l-4 shadow-sm hover:shadow-lg hover:shadow-cyan-500/10 transition-shadow",
        custom_attrs={"class": border_color},
    )


def biggest_gainer_card() -> rx.Component:
    return rx.el.div(
        rx.cond(
            StockState.biggest_gainer,
            rx.el.div(
                rx.el.div(
                    rx.icon("trending-up", class_name="h-6 w-6 text-green-400"),
                    class_name="p-3 bg-slate-800 rounded-lg",
                ),
                rx.el.div(
                    rx.el.p(
                        "Biggest Gainer",
                        class_name="text-sm font-medium text-slate-400",
                    ),
                    rx.el.div(
                        rx.el.p(
                            StockState.biggest_gainer["symbol"],
                            class_name="text-xl font-semibold text-slate-100",
                        ),
                        rx.el.p(
                            f"+{StockState.biggest_gainer['change'].to_string()}",
                            class_name="text-sm font-medium text-green-400",
                        ),
                        class_name="flex items-baseline gap-2",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex items-center gap-4 p-5 bg-[#151b28] rounded-lg border-l-4 border-green-500 shadow-sm hover:shadow-lg hover:shadow-cyan-500/10 transition-shadow",
            ),
            metric_card(
                "Biggest Gainer",
                "N/A",
                "trending-up",
                "h-6 w-6 text-slate-500",
                "border-slate-700",
            ),
        )
    )


def metric_cards() -> rx.Component:
    return rx.el.div(
        metric_card(
            "Total Stocks",
            StockState.total_stocks,
            "binary",
            "h-6 w-6 text-cyan-400",
            "border-cyan-500",
        ),
        metric_card(
            "Average Price",
            f"{SettingsState.currency_symbol}{StockState.average_price.to_string()}",
            "dollar-sign",
            "h-6 w-6 text-pink-400",
            "border-pink-500",
        ),
        metric_card(
            "Total Volume",
            StockState.total_volume.to_string(),
            "bar-chart-3",
            "h-6 w-6 text-purple-400",
            "border-purple-500",
        ),
        biggest_gainer_card(),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
    )