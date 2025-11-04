import reflex as rx
from app.states.import_state import ImportState, AvailableStock


def stock_selection_row(stock: AvailableStock) -> rx.Component:
    is_selected = ImportState.selected_stocks.contains(stock["symbol"])
    return rx.el.div(
        rx.el.div(
            rx.el.p(stock["symbol"], class_name="font-bold text-slate-100 text-sm"),
            rx.el.p(stock["name"], class_name="text-slate-400 text-xs truncate"),
            class_name="flex-1 truncate",
        ),
        rx.radix.checkbox(
            checked=is_selected,
            on_change=lambda _: ImportState.toggle_stock_selection(stock["symbol"]),
            high_contrast=True,
            size="3",
        ),
        on_click=lambda: ImportState.toggle_stock_selection(stock["symbol"]),
        class_name=rx.cond(
            is_selected,
            "flex items-center justify-between p-3 rounded-lg bg-cyan-500/10 border border-cyan-500 cursor-pointer",
            "flex items-center justify-between p-3 rounded-lg hover:bg-slate-800/50 cursor-pointer",
        ),
    )


def bulk_import_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                "Bulk Import Stocks",
                class_name="text-lg font-semibold text-slate-100 mb-4",
            ),
            rx.el.input(
                placeholder="Search by symbol or name...",
                on_change=ImportState.set_search_query.debounce(300),
                class_name="w-full px-3 py-2 bg-slate-800/50 border border-slate-700 rounded-md mb-4 focus:ring-2 focus:ring-cyan-500 text-sm",
            ),
            rx.el.div(
                rx.cond(
                    ImportState.is_loading,
                    rx.el.div(
                        rx.spinner(class_name="h-8 w-8 text-cyan-400"),
                        rx.el.p(
                            "Loading available stocks...",
                            class_name="text-slate-400 mt-2",
                        ),
                        class_name="flex flex-col items-center justify-center h-64",
                    ),
                    rx.el.div(
                        rx.foreach(
                            ImportState.filtered_available_stocks, stock_selection_row
                        ),
                        class_name="space-y-2",
                    ),
                ),
                class_name="h-96 overflow-y-auto pr-2",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=ImportState.toggle_dialog,
                        class_name="px-4 py-2 bg-slate-700 text-slate-200 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors",
                    )
                ),
                rx.el.button(
                    rx.cond(
                        ImportState.is_importing,
                        rx.spinner(class_name="h-4 w-4"),
                        f"Import {ImportState.selected_stocks.length()} Selected",
                    ),
                    on_click=ImportState.import_selected_stocks,
                    disabled=ImportState.is_importing
                    | (ImportState.selected_stocks.length() == 0),
                    class_name="px-4 py-2 bg-cyan-500 text-slate-900 rounded-md text-sm font-medium hover:bg-cyan-600 transition-colors flex items-center justify-center w-48 disabled:opacity-50",
                ),
                class_name="flex justify-end gap-3 mt-4 border-t border-slate-700 pt-4",
            ),
            style={
                "background": "rgba(21, 27, 40, 0.8)",
                "backdrop_filter": "blur(10px)",
                "border": "1px solid #2d3748",
                "width": "90vw",
                "max_width": "600px",
                "border_radius": "16px",
            },
        ),
        open=ImportState.show_dialog,
    )