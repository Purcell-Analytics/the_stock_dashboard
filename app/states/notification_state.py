import reflex as rx
from pydantic import BaseModel
import logging


class NotificationPreferences(BaseModel):
    price_alerts: bool = True
    alert_threshold: float = 5.0
    daily_summary: bool = False
    desktop_notifications: bool = False


class NotificationState(rx.State):
    notification_prefs_json: str = rx.LocalStorage(
        NotificationPreferences().model_dump_json(), name="notification_preferences"
    )
    _prefs: NotificationPreferences | None = None

    @rx.var
    def prefs(self) -> NotificationPreferences:
        if self._prefs is not None:
            return self._prefs
        if self.notification_prefs_json:
            try:
                self._prefs = NotificationPreferences.model_validate_json(
                    self.notification_prefs_json
                )
                return self._prefs
            except Exception as e:
                logging.exception(f"Failed to parse notification preferences: {e}")
        self._prefs = NotificationPreferences()
        return self._prefs

    def _update_prefs(self, new_prefs: NotificationPreferences):
        self._prefs = new_prefs
        self.notification_prefs_json = new_prefs.model_dump_json()

    @rx.event
    def set_price_alerts(self, enabled: bool):
        new_prefs = self.prefs.model_copy()
        new_prefs.price_alerts = enabled
        self._update_prefs(new_prefs)

    @rx.event
    def set_alert_threshold(self, threshold: str):
        try:
            new_prefs = self.prefs.model_copy()
            new_prefs.alert_threshold = float(threshold)
            self._update_prefs(new_prefs)
        except ValueError as e:
            logging.exception(f"Invalid threshold value: {threshold}, error: {e}")

    @rx.event
    def set_daily_summary(self, enabled: bool):
        new_prefs = self.prefs.model_copy()
        new_prefs.daily_summary = enabled
        self._update_prefs(new_prefs)

    @rx.event
    def set_desktop_notifications(self, enabled: bool):
        new_prefs = self.prefs.model_copy()
        new_prefs.desktop_notifications = enabled
        self._update_prefs(new_prefs)
        if enabled:
            return rx.call_script("Notification.requestPermission()")