import uuid
from typing import Dict, Any, List, Optional
from ..models.environmental_state import EnvironmentalState
from ..services.db_service import db_service

class SessionMemory:
    """
    Maintains multi-turn conversational context and cumulative environmental profiles.
    """

    def __init__(self):
        self._in_memory_sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        cid = conversation_id or str(uuid.uuid4())
        
        if cid in self._in_memory_sessions:
            return self._in_memory_sessions[cid]

        # Check SQLite
        persisted = db_service.get_conversation(cid)
        if persisted:
            session_data = {
                "conversation_id": cid,
                "accumulated_state": persisted.get("accumulated_state", {}),
                "messages": persisted.get("messages_history", [])
            }
            self._in_memory_sessions[cid] = session_data
            return session_data

        # New session
        new_session = {
            "conversation_id": cid,
            "accumulated_state": {},
            "messages": []
        }
        self._in_memory_sessions[cid] = new_session
        return new_session

    def update_session_state(
        self,
        conversation_id: str,
        new_variables: Dict[str, Any]
    ) -> EnvironmentalState:
        session = self.get_or_create_session(conversation_id)
        current_state_dict = session.get("accumulated_state", {})

        # Merge newly extracted variables
        for k, v in new_variables.items():
            if v is not None:
                current_state_dict[k] = v

        session["accumulated_state"] = current_state_dict
        
        # Persist to database
        db_service.save_conversation(
            conversation_id=conversation_id,
            accumulated_state=current_state_dict,
            messages=session.get("messages", [])
        )

        return EnvironmentalState(**current_state_dict)

    def record_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str
    ):
        session = self.get_or_create_session(conversation_id)
        session["messages"].append({"role": "user", "content": user_message})
        session["messages"].append({"role": "assistant", "content": assistant_response})

        db_service.save_conversation(
            conversation_id=conversation_id,
            accumulated_state=session.get("accumulated_state", {}),
            messages=session["messages"]
        )

    def get_accumulated_state(self, conversation_id: str) -> EnvironmentalState:
        session = self.get_or_create_session(conversation_id)
        return EnvironmentalState(**session.get("accumulated_state", {}))

session_memory = SessionMemory()
