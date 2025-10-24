import reflex as rx
from app.util.supabase_client import get_supabase_client
import logging


class FeedbackState(rx.State):
    category: str = ""
    message: str = ""
    is_submitting: bool = False

    @rx.event
    def reset_form(self):
        self.category = ""
        self.message = ""

    @rx.event(background=True)
    async def submit_feedback(self):
        if not self.category or not self.message.strip():
            yield rx.toast(
                "Please select a category and write a message.", duration=4000
            )
            return
        async with self:
            self.is_submitting = True
        try:
            client = get_supabase_client()
            if not client:
                async with self:
                    self.is_submitting = False
                yield rx.toast("Database connection not available.", duration=5000)
                return
            client.table("feedback").insert(
                {"category": self.category, "message": self.message}
            ).execute()
            yield rx.toast("Thank you for your feedback!", duration=3000)
            async with self:
                self.reset_form()
        except Exception as e:
            logging.exception(f"Error submitting feedback: {e}")
            yield rx.toast(f"Failed to submit feedback: {e}", duration=5000)
        finally:
            async with self:
                self.is_submitting = False