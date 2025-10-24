import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stock_table import (
    stock_table,
    skeleton_loader,
    empty_state,
    stock_row,
)
from app.components.add_stock_dialog import add_stock_dialog
from app.states.stock_state import StockState
from app.states.watchlist_state import WatchlistState
from app.states.settings_state import SettingsState
from app.states.data_state import DataState
from app.states.profile_state import ProfileState
from app.states.notification_state import NotificationState
from app.states.feedback_state import FeedbackState
from app.states.api_state import ApiState
from app.components.metric_cards import metric_card, metric_cards


def page_layout(content: rx.Component, title: str) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            header(),
            rx.el.main(content, add_stock_dialog(), class_name="p-6"),
            on_mount=[SettingsState.on_load, ProfileState.on_load_profile],
            class_name="flex-1 flex flex-col h-screen overflow-y-auto",
        ),
        class_name=rx.cond(
            SettingsState.preferences.theme == "dark",
            "flex bg-[#0a0f1a] text-slate-200 font-['Inter']",
            "flex bg-slate-50 text-slate-800 font-['Inter']",
        ),
    )


def index() -> rx.Component:
    return page_layout(
        rx.el.div(
            metric_cards(),
            rx.el.div(
                rx.cond(
                    StockState.is_loading,
                    rx.el.div(
                        skeleton_loader(),
                        skeleton_loader(),
                        skeleton_loader(),
                        skeleton_loader(),
                        class_name="bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
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
                                class_name="font-bold text-lg text-slate-300",
                            ),
                            rx.el.p(
                                StockState.error_message,
                                class_name="text-sm text-slate-500",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 bg-yellow-900/20 rounded-lg border border-yellow-700/50",
                        ),
                        rx.cond(
                            StockState.stocks.length() > 0, stock_table(), empty_state()
                        ),
                    ),
                ),
                class_name="mt-6",
            ),
        ),
        title="Dashboard",
    )


def watchlist() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.div(
                metric_card(
                    "Watchlist Stocks",
                    WatchlistState.total_watchlist_stocks.to_string(),
                    "star",
                    "text-yellow-400",
                    "border-yellow-500",
                ),
                metric_card(
                    "Avg. Change",
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        f"+{WatchlistState.average_watchlist_change.to_string()}",
                        WatchlistState.average_watchlist_change.to_string(),
                    ),
                    "trending-up",
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        "text-green-400",
                        "text-red-400",
                    ),
                    rx.cond(
                        WatchlistState.average_watchlist_change >= 0,
                        "border-green-500",
                        "border-red-500",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            rx.el.div(
                rx.cond(
                    WatchlistState.is_loading,
                    rx.el.div(
                        skeleton_loader(),
                        skeleton_loader(),
                        class_name="bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
                    ),
                    rx.cond(
                        WatchlistState.watchlist_stocks.length() > 0,
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Stock",
                                        class_name="text-left font-semibold text-slate-400 uppercase text-xs tracking-wider pl-6 py-3",
                                    ),
                                    rx.el.th(
                                        "Price",
                                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Change",
                                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                                    ),
                                    rx.el.th(
                                        "Volume",
                                        class_name="text-right font-semibold text-slate-400 uppercase text-xs tracking-wider",
                                    ),
                                    rx.el.th("", class_name="pr-6 py-3"),
                                    class_name="bg-slate-800/50",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(WatchlistState.watchlist_stocks, stock_row)
                            ),
                            class_name="w-full",
                        ),
                        empty_state(),
                    ),
                ),
                class_name="mt-6 bg-[#151b28] rounded-lg border border-slate-800 overflow-hidden",
            ),
        ),
        title="Watchlist",
    )


def settings_card(*children, **props) -> rx.Component:
    return rx.el.div(
        *children,
        class_name=rx.cond(
            SettingsState.preferences.theme == "dark",
            "bg-[#151b28] p-6 rounded-lg border border-slate-800 mb-6",
            "bg-white p-6 rounded-lg border border-slate-200 mb-6",
        ),
        **props,
    )


def profile_card() -> rx.Component:
    return settings_card(
        rx.el.h3(
            "User Profile",
            class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    ProfileState.user_initials,
                    class_name="w-16 h-16 rounded-full bg-cyan-500 flex items-center justify-center text-2xl font-bold text-slate-900",
                ),
                rx.cond(
                    ProfileState.is_editing_name,
                    rx.el.div(
                        rx.el.input(
                            default_value=ProfileState.temp_display_name,
                            on_change=ProfileState.set_temp_display_name,
                            class_name="bg-slate-700 border border-slate-600 rounded-md px-3 py-1.5 text-base font-medium text-slate-100 focus:ring-2 focus:ring-cyan-500",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("x", class_name="h-4 w-4"),
                                on_click=ProfileState.cancel_editing_name,
                                class_name="p-2 text-slate-400 hover:bg-slate-700 rounded-md",
                            ),
                            rx.el.button(
                                rx.icon("check", class_name="h-4 w-4"),
                                on_click=ProfileState.save_display_name,
                                class_name="p-2 text-green-400 hover:bg-slate-700 rounded-md",
                            ),
                            class_name="flex items-center gap-1",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.div(
                        rx.el.p(
                            ProfileState.profile.display_name,
                            class_name="text-xl font-semibold text-slate-100",
                        ),
                        rx.el.button(
                            rx.icon("pencil", class_name="h-4 w-4"),
                            on_click=ProfileState.start_editing_name,
                            class_name="p-2 text-slate-400 hover:text-cyan-400 hover:bg-slate-700 rounded-md",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name="flex-1 flex flex-col gap-2",
            ),
            class_name="flex items-center gap-6",
        ),
    )


def settings() -> rx.Component:
    return page_layout(
        rx.el.div(
            rx.el.h2("Settings", class_name="text-2xl font-bold text-slate-100 mb-6"),
            profile_card(),
            settings_card(
                rx.el.h3(
                    "API Integration",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Auto-Sync", class_name="font-medium"),
                        rx.radix.switch(
                            checked=SettingsState.preferences.auto_sync_enabled,
                            on_change=SettingsState.set_auto_sync_enabled,
                            high_contrast=True,
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.p("Last Sync", class_name="font-medium text-slate-400"),
                        rx.el.p(ApiState.last_sync_time, class_name="font-semibold"),
                        class_name="flex items-center justify-between py-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Successful Syncs", class_name="font-medium text-slate-400"
                        ),
                        rx.el.p(
                            ApiState.sync_success_count, class_name="font-semibold"
                        ),
                        class_name="flex items-center justify-between py-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Failed Syncs", class_name="font-medium text-slate-400"
                        ),
                        rx.el.p(ApiState.sync_error_count, class_name="font-semibold"),
                        class_name="flex items-center justify-between py-2",
                    ),
                ),
            ),
            settings_card(
                rx.el.h3(
                    "User Preferences",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Theme", class_name="font-medium"),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("sun"),
                                on_click=lambda: SettingsState.set_theme("light"),
                                class_name=rx.cond(
                                    SettingsState.preferences.theme == "light",
                                    "p-2 rounded-l-md bg-cyan-500 text-white",
                                    "p-2 rounded-l-md bg-slate-700 hover:bg-slate-600",
                                ),
                            ),
                            rx.el.button(
                                rx.icon("moon"),
                                on_click=lambda: SettingsState.set_theme("dark"),
                                class_name=rx.cond(
                                    SettingsState.preferences.theme == "dark",
                                    "p-2 rounded-r-md bg-cyan-500 text-white",
                                    "p-2 rounded-r-md bg-slate-700 hover:bg-slate-600",
                                ),
                            ),
                            class_name="flex",
                        ),
                        class_name="flex items-center justify-between py-3",
                    ),
                    rx.el.div(
                        rx.el.label("Currency", class_name="font-medium"),
                        rx.el.select(
                            rx.el.option("USD", value="USD"),
                            rx.el.option("EUR", value="EUR"),
                            rx.el.option("GBP", value="GBP"),
                            value=SettingsState.preferences.currency,
                            on_change=SettingsState.set_currency,
                            class_name="bg-slate-700 rounded-md px-2 py-1",
                        ),
                        class_name="flex items-center justify-between py-3",
                    ),
                    rx.el.div(
                        rx.el.label("Refresh Interval", class_name="font-medium"),
                        rx.el.select(
                            rx.el.option("30 seconds", value="30"),
                            rx.el.option("1 minute", value="60"),
                            rx.el.option("5 minutes", value="300"),
                            rx.el.option("Manual", value="0"),
                            value=SettingsState.preferences.refresh_interval.to_string(),
                            on_change=SettingsState.set_refresh_interval,
                            class_name="bg-slate-700 rounded-md px-2 py-1",
                        ),
                        class_name="flex items-center justify-between py-3",
                    ),
                ),
            ),
            settings_card(
                rx.el.h3(
                    "Data Management",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Export Data", class_name="font-medium"),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("download", class_name="h-4 w-4 mr-2"),
                                "Export as CSV",
                                on_click=DataState.export_data("csv"),
                                class_name="flex items-center text-sm px-3 py-1.5 bg-slate-700 hover:bg-slate-600 rounded-md",
                            ),
                            rx.el.button(
                                rx.icon("download", class_name="h-4 w-4 mr-2"),
                                "Export as JSON",
                                on_click=DataState.export_data("json"),
                                class_name="flex items-center text-sm px-3 py-1.5 bg-slate-700 hover:bg-slate-600 rounded-md",
                            ),
                            class_name="flex gap-2",
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.p("Clear Watchlist", class_name="font-medium"),
                        rx.el.button(
                            "Clear Watchlist",
                            on_click=DataState.clear_watchlist,
                            class_name="text-sm px-3 py-1.5 bg-yellow-600/20 text-yellow-300 border border-yellow-500/50 hover:bg-yellow-600/30 rounded-md",
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.p("Clear All Stocks", class_name="font-medium"),
                        rx.el.button(
                            "Clear All Stocks",
                            on_click=DataState.set_show_clear_stocks_dialog(True),
                            class_name="text-sm px-3 py-1.5 bg-red-600/20 text-red-300 border border-red-500/50 hover:bg-red-600/30 rounded-md",
                        ),
                        class_name="flex items-center justify-between py-3",
                    ),
                ),
            ),
            settings_card(
                rx.el.h3(
                    "Data Statistics",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Total Records", class_name="font-medium text-slate-400"
                        ),
                        rx.el.p(DataState.total_records, class_name="font-semibold"),
                        class_name="flex items-center justify-between py-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Last Updated", class_name="font-medium text-slate-400"
                        ),
                        rx.el.p(DataState.last_updated, class_name="font-semibold"),
                        class_name="flex items-center justify-between py-2",
                    ),
                ),
                rx.radix.primitives.dialog.root(
                    rx.radix.primitives.dialog.trigger(rx.el.div()),
                    rx.radix.primitives.dialog.content(
                        rx.radix.primitives.dialog.title(
                            "Confirm Deletion",
                            class_name="text-lg font-semibold text-slate-100",
                        ),
                        rx.el.p(
                            "Are you sure you want to delete all stocks? This action is irreversible.",
                            class_name="text-sm text-slate-400 my-4",
                        ),
                        rx.el.div(
                            rx.radix.primitives.dialog.close(
                                rx.el.button(
                                    "Cancel",
                                    type="button",
                                    on_click=DataState.set_show_clear_stocks_dialog(
                                        False
                                    ),
                                    class_name="px-4 py-2 bg-slate-700 text-slate-200 rounded-md text-sm font-medium hover:bg-slate-600 transition-colors",
                                )
                            ),
                            rx.el.button(
                                "Yes, Delete All",
                                on_click=[
                                    DataState.clear_all_stocks,
                                    DataState.set_show_clear_stocks_dialog(False),
                                ],
                                class_name="px-4 py-2 bg-red-500 text-white rounded-md text-sm font-medium hover:bg-red-600 transition-colors",
                            ),
                            class_name="flex justify-end gap-3 mt-4",
                        ),
                        style={
                            "background": "rgba(21, 27, 40, 0.8)",
                            "backdrop_filter": "blur(10px)",
                            "border": "1px solid #2d3748",
                            "max_width": "450px",
                            "border_radius": "16px",
                        },
                    ),
                    open=DataState.show_clear_stocks_dialog,
                ),
            ),
            settings_card(
                rx.el.h3(
                    "About",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.h3(
                    "Notification Preferences",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Price Change Alerts", class_name="font-medium"),
                        rx.radix.switch(
                            checked=NotificationState.prefs.price_alerts,
                            on_change=NotificationState.set_price_alerts,
                            high_contrast=True,
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.label("Alert Threshold (%) ", class_name="font-medium"),
                        rx.el.input(
                            default_value=NotificationState.prefs.alert_threshold.to_string(),
                            on_change=NotificationState.set_alert_threshold,
                            type="number",
                            class_name="bg-slate-700 rounded-md px-2 py-1 w-20 text-right",
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.label("Daily Summary Email", class_name="font-medium"),
                        rx.radix.switch(
                            checked=NotificationState.prefs.daily_summary,
                            on_change=NotificationState.set_daily_summary,
                            high_contrast=True,
                        ),
                        class_name="flex items-center justify-between py-3 border-b border-slate-800/50",
                    ),
                    rx.el.div(
                        rx.el.label("Desktop Notifications", class_name="font-medium"),
                        rx.radix.switch(
                            checked=NotificationState.prefs.desktop_notifications,
                            on_change=NotificationState.set_desktop_notifications,
                            high_contrast=True,
                        ),
                        class_name="flex items-center justify-between py-3",
                    ),
                ),
            ),
            settings_card(
                rx.el.h3(
                    "Submit Feedback",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.form(
                    rx.el.select(
                        rx.el.option("Select Category...", value="", disabled=True),
                        rx.el.option("Bug Report", value="bug"),
                        rx.el.option("Feature Request", value="feature"),
                        rx.el.option("General Feedback", value="general"),
                        value=FeedbackState.category,
                        on_change=FeedbackState.set_category,
                        class_name="w-full bg-slate-700 rounded-md px-2 py-2 mb-3 text-sm",
                    ),
                    rx.el.textarea(
                        on_change=FeedbackState.set_message,
                        placeholder="Tell us what you think...",
                        class_name="w-full bg-slate-700 rounded-md px-3 py-2 text-sm h-24 mb-3",
                        default_value=FeedbackState.message,
                    ),
                    rx.el.button(
                        rx.cond(
                            FeedbackState.is_submitting,
                            rx.spinner(class_name="mr-2"),
                            None,
                        ),
                        "Submit Feedback",
                        type="submit",
                        disabled=FeedbackState.is_submitting,
                        class_name="w-full flex items-center justify-center text-sm px-3 py-2 bg-cyan-500 text-slate-900 font-semibold hover:bg-cyan-600 rounded-md transition-colors",
                    ),
                    on_submit=FeedbackState.submit_feedback,
                    width="100%",
                ),
            ),
            settings_card(
                rx.el.h3(
                    "About",
                    class_name="text-lg font-semibold mb-4 border-b border-slate-700 pb-2",
                ),
                rx.el.p("StockDash v1.0.0", class_name="text-slate-400"),
            ),
        ),
        title="Settings",
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
app.add_page(watchlist)
app.add_page(settings)