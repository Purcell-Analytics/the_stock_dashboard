import reflex as rx


def nav_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium text-sm"),
            class_name="flex items-center gap-3",
        ),
        href=url,
        class_name="flex items-center p-3 rounded-lg text-gray-700 hover:bg-violet-100/50 hover:text-violet-800 transition-colors duration-200",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("candlestick-chart", class_name="h-8 w-8 text-violet-600"),
                rx.el.span("StockDash", class_name="text-xl font-bold text-gray-800"),
                class_name="flex items-center gap-3 px-4 h-16 border-b",
            ),
            rx.el.nav(
                nav_item("Dashboard", "layout-dashboard", "/"),
                nav_item("Watchlist", "star", "#"),
                nav_item("Settings", "settings", "#"),
                class_name="flex-1 p-4 space-y-2",
            ),
        ),
        class_name="hidden md:flex flex-col w-64 bg-white border-r",
    )