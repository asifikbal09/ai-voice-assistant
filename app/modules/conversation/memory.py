from typing import Dict, List


class ConversationMemory:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.sessions: Dict[str, List[dict]] = {}

    def get_history(self, session_id: str) -> List[dict]:
        return self.sessions.get(session_id, [])

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append(
            {
                "role": role,
                "content": content,
            }
        )

        self.sessions[session_id] = self.sessions[session_id][
            -self.max_messages:
        ]

    def clear_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)


conversation_memory = ConversationMemory(max_messages=10)