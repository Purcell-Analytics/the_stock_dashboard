import reflex as rx
from typing import Literal
from pydantic import BaseModel
import json
import logging
import uuid


class UserPreferences(BaseModel):
    theme: Literal["light", "dark"] = "dark"
    currency: Literal["USD", "EUR", "GBP"] = "USD"
    refresh_interval: int = 30
    auto_sync_enabled: bool = True


class SettingsState(rx.State):
    preferences_json: str = rx.LocalStorage(
        UserPreferences().model_dump_json(), name="user_preferences"
    )
    _preferences: UserPreferences | None = None
    _refresh_task_id: str = ""

    @rx.var
    def preferences(self) -> UserPreferences:
        if self._preferences is not None:
            return self._preferences
        if self.preferences_json:
            try:
                self._preferences = UserPreferences.model_validate_json(
                    self.preferences_json
                )
                return self._preferences
            except Exception as e:
                logging.exception(f"Failed to parse user preferences: {e}")
        self._preferences = UserPreferences(theme="dark")
        return self._preferences

    @rx.var
    def currency_symbol(self) -> str:
        symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
        return symbols.get(self.preferences.currency, "$")

    @rx.event
    def on_load(self):
        if not self.preferences_json:
            self.preferences_json = UserPreferences(theme="dark").model_dump_json()
        else:
            _ = self.preferences
        return SettingsState.start_refresh_task()

    def _update_preferences(self, new_prefs: UserPreferences):
        self._preferences = new_prefs
        self.preferences_json = new_prefs.model_dump_json()

    @rx.event
    def set_theme(self, theme: str):
        if theme in ["light", "dark"]:
            new_prefs = self.preferences.model_copy()
            new_prefs.theme = theme
            self._update_preferences(new_prefs)

    @rx.event
    def set_currency(self, currency: str):
        if currency in ["USD", "EUR", "GBP"]:
            new_prefs = self.preferences.model_copy()
            new_prefs.currency = currency
            self._update_preferences(new_prefs)

    @rx.event
    def set_refresh_interval(self, interval: str):
        try:
            interval_val = int(interval)
            if interval_val in [30, 60, 300, 0]:
                new_prefs = self.preferences.model_copy()
                new_prefs.refresh_interval = interval_val
                self._update_preferences(new_prefs)
                return SettingsState.start_refresh_task()
        except ValueError as e:
            logging.exception(f"Invalid refresh interval: {interval}, error: {e}")

    @rx.event
    def set_auto_sync_enabled(self, enabled: bool):
        new_prefs = self.preferences.model_copy()
        new_prefs.auto_sync_enabled = enabled
        self._update_preferences(new_prefs)
        return SettingsState.start_refresh_task()

    @rx.event
    def start_refresh_task(self):
        """Starts or restarts the background data refresh task."""
        from app.states.stock_state import StockState
        from app.states.api_state import ApiState

        if self._refresh_task_id:
            yield rx.call_script(f"clearInterval(window.{self._refresh_task_id})")
        interval = self.preferences.refresh_interval
        if interval > 0:
            task_id = f"stock_refresh_task_{str(uuid.uuid4()).replace('-', '')}"
            if self.preferences.auto_sync_enabled:
                event_trigger = f"app.states.api_state.ApiState.sync_all_stocks"
            else:
                event_trigger = f"app.states.stock_state.StockState.fetch_stocks(true)"
            code = f"window.{task_id} = setInterval(() => _reflex.callEvent('{event_trigger}', {{}}), {interval * 1000})"
            yield rx.call_script(
                code, callback=lambda: SettingsState.set_refresh_task_id(task_id)
            )
        else:
            self._refresh_task_id = ""

    @rx.event
    def set_refresh_task_id(self, task_id: str):
        self._refresh_task_id = task_id