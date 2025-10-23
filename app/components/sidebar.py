import reflex as rx
from app.states.stock_state import StockState


def nav_item(text: str, icon: str, url: str) -> rx.Component:
    is_active = StockState.router.page.path == url
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="w-5 h-5"),
            rx.el.span(text, class_name="font-medium text-sm"),
            class_name="flex items-center gap-3",
        ),
        href=url,
        class_name=rx.cond(
            is_active,
            "flex items-center p-3 rounded-lg bg-cyan-500/10 text-cyan-400 transition-colors duration-200",
            "flex items-center p-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors duration-200",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("candlestick-chart", class_name="h-8 w-8 text-cyan-400"),
                rx.el.span("StockDash", class_name="text-xl font-bold text-slate-100"),
                class_name="flex items-center gap-3 px-4 h-16 border-b border-slate-800",
            ),
            rx.el.nav(
                nav_item("Dashboard", "layout-dashboard", "/"),
                nav_item("Watchlist", "star", "/watchlist"),
                nav_item("Settings", "settings", "/settings"),
                class_name="flex-1 p-4 space-y-2",
            ),
        ),
        class_name="hidden md:flex flex-col w-64 bg-[#0f1419] border-r border-slate-800 h-screen",
    )