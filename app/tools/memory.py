import json
from datetime import datetime
from typing import Optional

class MemoryStore:
    """用户记忆存储 (传统 API: SQLite)"""
    def __init__(self, db_path: str = "data/travel.db"):
        self._sessions: dict[str, list[dict]] = {}
        self._preferences: dict[str, dict] = {}
        self.db_path = db_path

    def add_message(self, session_id: str, role: str, content: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append({"role": role, "content": content, "timestamp": datetime.now().isoformat()})

    def get_history(self, session_id: str, limit: int = 20) -> list[dict]:
        return self._sessions.get(session_id, [])[-limit:]

    def save_preference(self, session_id: str, key: str, value: any) -> None:
        if session_id not in self._preferences:
            self._preferences[session_id] = {}
        self._preferences[session_id][key] = value

    def get_preference(self, session_id: str, key: str) -> Optional[any]:
        return self._preferences.get(session_id, {}).get(key)

    def get_all_preferences(self, session_id: str) -> dict:
        return self._preferences.get(session_id, {})
