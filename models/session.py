"""Session management for user conversations."""
from datetime import datetime
from config import MAX_HISTORY_LENGTH, DEFAULT_MODE


class UserSession:
    """Manages individual user session data."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.messages = []
        self.jarvis_mode = False
        self.mode = DEFAULT_MODE
        self.created_at = datetime.now()
        self.message_count = 0
        self.search_count = 0
        self.code_count = 0

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > MAX_HISTORY_LENGTH * 2:
            self.messages = self.messages[-MAX_HISTORY_LENGTH * 2:]
        if role == "user":
            self.message_count += 1

    def clear_history(self):
        """Clear conversation history."""
        self.messages = []

    def toggle_jarvis_mode(self) -> bool:
        """Toggle Jarvis mode on/off."""
        self.jarvis_mode = not self.jarvis_mode
        return self.jarvis_mode

    def set_mode(self, mode: str) -> bool:
        """Set bot mode (online/offline)."""
        if mode in ["online", "offline"]:
            self.mode = mode
            return True
        return False

    def get_stats(self) -> dict:
        """Get session statistics."""
        return {
            "user_id": self.user_id,
            "message_count": self.message_count,
            "search_count": self.search_count,
            "code_count": self.code_count,
            "jarvis_mode": self.jarvis_mode,
            "mode": self.mode,
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M"),
            "history_length": len(self.messages),
        }


class SessionManager:
    """Manages all user sessions."""

    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id: int) -> UserSession:
        """Get or create a user session."""
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id)
        return self.sessions[user_id]

    def clear_session(self, user_id: int):
        """Clear a user's session history."""
        if user_id in self.sessions:
            self.sessions[user_id].clear_history()
