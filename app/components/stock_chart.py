import reflex as rx
from app.states.chart_state import ChartState, Timeframe
from app.states.settings_state import SettingsState


def timeframe_button(timeframe: Timeframe, label: str) -> rx.Component:
    is_active = ChartState.selected_timeframe == timeframe
    return rx.el.button(
        label,
        on_click=lambda: ChartState.set_timeframe(timeframe),
        class_name=rx.cond(
            is_active,
            "px-3 py-1 text-sm font-semibold text-slate-900 bg-cyan-400 rounded-md",
            "px-3 py-1 text-sm font-medium text-slate-400 hover:bg-slate-700/50 rounded-md",
        ),
        disabled=ChartState.is_loading_chart,
    )


def timeframe_selector() -> rx.Component:
    return rx.el.div(
        timeframe_button("1D", "1D"),
        timeframe_button("1W", "1W"),
        timeframe_button("1M", "1M"),
        timeframe_button("3M", "3M"),
        timeframe_button("6M", "6M"),
        timeframe_button("1Y", "1Y"),
        timeframe_button("ALL", "ALL"),
        class_name="flex items-center gap-2",
    )


def stock_chart_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    f"{ChartState.selected_symbol} Price History",
                    class_name="text-lg font-semibold text-slate-100",
                ),
                timeframe_selector(),
                class_name="flex justify-between items-center mb-4",
            ),
            rx.el.div(
                rx.cond(
                    ChartState.is_loading_chart,
                    rx.el.div(
                        rx.el.div(
                            rx.spinner(class_name="h-8 w-8 text-cyan-400"),
                            rx.el.p(
                                "Loading Chart Data...",
                                class_name="text-slate-400 mt-2",
                            ),
                            class_name="flex flex-col items-center justify-center h-full",
                        ),
                        class_name="h-96 w-full bg-slate-800/50 rounded-lg animate-pulse",
                    ),
                    rx.cond(
                        ChartState.chart_error_message,
                        rx.el.div(
                            rx.icon(
                                "flag_triangle_right",
                                class_name="h-10 w-10 text-yellow-500",
                            ),
                            rx.el.p(
                                "Error Loading Chart",
                                class_name="font-semibold text-slate-200 mt-2",
                            ),
                            rx.el.p(
                                ChartState.chart_error_message,
                                class_name="text-sm text-slate-500",
                            ),
                            class_name="h-96 flex flex-col items-center justify-center text-center",
                        ),
                        rx.cond(
                            ChartState.chart_data.length() > 0,
                            rx.el.div(
                                rx.recharts.composed_chart(
                                    rx.recharts.cartesian_grid(
                                        stroke_dasharray="3 3",
                                        stroke="#374151",
                                        vertical=False,
                                    ),
                                    rx.recharts.graphing_tooltip(
                                        cursor={"fill": "rgba(100, 100, 100, 0.1)"}
                                    ),
                                    rx.recharts.x_axis(
                                        data_key="date",
                                        tick_line=False,
                                        axis_line=False,
                                        stroke="#9ca3af",
                                        tick_margin=8,
                                        custom_attrs={"fontSize": 12},
                                    ),
                                    rx.recharts.y_axis(
                                        y_axis_id="left",
                                        orientation="left",
                                        domain=["auto", "auto"],
                                        tick_line=False,
                                        axis_line=False,
                                        stroke="#9ca3af",
                                        tick_margin=8,
                                        custom_attrs={"fontSize": 12},
                                    ),
                                    rx.recharts.y_axis(
                                        y_axis_id="right",
                                        orientation="right",
                                        domain=["auto", "auto"],
                                        tick_line=False,
                                        axis_line=False,
                                        stroke="#9ca3af",
                                        tick_margin=8,
                                        custom_attrs={"fontSize": 12},
                                    ),
                                    rx.recharts.line(
                                        data_key="close",
                                        stroke="#22d3ee",
                                        stroke_width=2,
                                        dot=False,
                                        type_="natural",
                                        y_axis_id="left",
                                        name="Price",
                                    ),
                                    rx.recharts.bar(
                                        data_key="volume",
                                        fill="#38bdf8",
                                        fill_opacity=0.2,
                                        y_axis_id="right",
                                        name="Volume",
                                    ),
                                    data=ChartState.chart_data,
                                    height=400,
                                    width="100%",
                                    margin={
                                        "top": 5,
                                        "right": 20,
                                        "bottom": 5,
                                        "left": 20,
                                    },
                                ),
                                height="400px",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "bar-chart-2", class_name="h-10 w-10 text-slate-500"
                                ),
                                rx.el.p(
                                    "No Data Available",
                                    class_name="font-semibold text-slate-200 mt-2",
                                ),
                                rx.el.p(
                                    "Could not retrieve historical data for this stock.",
                                    class_name="text-sm text-slate-500",
                                ),
                                class_name="h-96 flex flex-col items-center justify-center text-center",
                            ),
                        ),
                    ),
                )
            ),
        ),
        class_name="bg-[#151b28] p-6 rounded-lg border border-slate-800",
    )