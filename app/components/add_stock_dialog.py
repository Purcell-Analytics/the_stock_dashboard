import reflex as rx
from app.states.stock_state import StockState


def form_field(
    label: str, placeholder: str, name: str, type: str, value: rx.Var[str]
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="text-sm font-medium text-slate-300 mb-1 block"),
        rx.el.input(
            placeholder=placeholder,
            name=name,
            type=type,
            default_value=value,
            class_name="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-md focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-colors text-sm text-slate-100 placeholder:text-slate-500",
        ),
        class_name="mb-4",
    )


def add_stock_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.content(
            rx.el.form(
                rx.radix.primitives.dialog.title(
                    "Add New Stock",
                    class_name="text-lg font-semibold text-slate-100 mb-4",
                ),
                rx.el.p(
                    StockState.error_message, class_name="text-red-400 text-sm mb-3"
                ),
                form_field(
                    "Symbol", "e.g. AAPL", "symbol", "text", StockState.form_symbol
                ),
                form_field(
                    "Name", "e.g. Apple Inc.", "name", "text", StockState.form_name
                ),
                form_field(
                    "Price", "e.g. 150.25", "price", "number", StockState.form_price
                ),
                form_field(
                    "Change", "e.g. 1.50", "change", "number", StockState.form_change
                ),
                form_field(
                    "Volume", "e.g. 1000000", "volume", "number", StockState.form_volume
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=StockState.toggle_add_stock_dialog,
                            class_name="px-4 py-2 bg-slate-700 text-slate-200 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors",
                        )
                    ),
                    rx.el.button(
                        "Add Stock",
                        type="submit",
                        class_name="px-4 py-2 bg-cyan-500 text-slate-900 rounded-md text-sm font-medium hover:bg-cyan-600 transition-colors",
                    ),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=StockState.add_stock,
            ),
            style={
                "background": "rgba(21, 27, 40, 0.8)",
                "backdrop_filter": "blur(10px)",
                "border": "1px solid #2d3748",
                "max_width": "450px",
                "border_radius": "16px",
            },
        ),
        open=StockState.show_add_stock_dialog,
    )