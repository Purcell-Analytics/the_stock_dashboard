import reflex as rx
from pydantic import BaseModel
import logging


class UserProfile(BaseModel):
    display_name: str = "User"


class ProfileState(rx.State):
    profile_json: str = rx.LocalStorage(
        UserProfile().model_dump_json(), name="user_profile"
    )
    _profile: UserProfile | None = None
    is_editing_name: bool = False
    temp_display_name: str = ""

    @rx.var
    def profile(self) -> UserProfile:
        if self._profile is not None:
            return self._profile
        if self.profile_json:
            try:
                self._profile = UserProfile.model_validate_json(self.profile_json)
                return self._profile
            except Exception as e:
                logging.exception(f"Failed to parse user profile: {e}")
        self._profile = UserProfile()
        return self._profile

    @rx.var
    def user_initials(self) -> str:
        name = self.profile.display_name
        if not name or not name.strip():
            return "U"
        parts = name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return parts[0][0].upper()

    def _update_profile(self, new_profile: UserProfile):
        self._profile = new_profile
        self.profile_json = new_profile.model_dump_json()

    @rx.event
    def on_load_profile(self):
        if not self.profile_json:
            self.profile_json = UserProfile().model_dump_json()
        else:
            _ = self.profile

    @rx.event
    def start_editing_name(self):
        self.is_editing_name = True
        self.temp_display_name = self.profile.display_name

    @rx.event
    def cancel_editing_name(self):
        self.is_editing_name = False

    @rx.event
    def save_display_name(self):
        if self.temp_display_name.strip():
            new_profile = self.profile.model_copy()
            new_profile.display_name = self.temp_display_name
            self._update_profile(new_profile)
        self.is_editing_name = False