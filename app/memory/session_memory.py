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

    def get_structured_context(self, conversation_id: str) -> Dict[str, Any]:
        """
        Returns structured environmental context segmented into domains
        as specified in Hackathon Section 7.
        """
        session = self.get_or_create_session(conversation_id)
        accumulated = session.get("accumulated_state", {})
        
        return {
            "conversation_id": conversation_id,
            "location": {
                k: accumulated[k] for k in ["location_name", "latitude", "longitude", "region", "country", "climate_zone"]
                if k in accumulated and accumulated[k] is not None
            },
            "soil": {
                k: accumulated[k] for k in ["soil_ph", "soil_organic_carbon", "soil_moisture"]
                if k in accumulated and accumulated[k] is not None
            },
            "water": {
                k: accumulated[k] for k in ["water_availability", "irrigation", "water_stress"]
                if k in accumulated and accumulated[k] is not None
            },
            "vegetation": {
                k: accumulated[k] for k in ["monoculture_or_polyculture", "habitat_diversity", "land_cover"]
                if k in accumulated and accumulated[k] is not None
            },
            "land_use": {
                k: accumulated[k] for k in ["land_use", "habitat_fragmentation", "land_disturbance", "pesticide_intensity", "deforestation_level"]
                if k in accumulated and accumulated[k] is not None
            },
            "biodiversity": {
                k: accumulated[k] for k in ["species_richness", "species_diversity", "pollinator_presence", "microbial_diversity"]
                if k in accumulated and accumulated[k] is not None
            },
            "climate": {
                k: accumulated[k] for k in ["temperature", "rainfall", "rainfall_variability", "drought_condition"]
                if k in accumulated and accumulated[k] is not None
            },
            "conversation_history": session.get("messages", [])
        }

session_memory = SessionMemory()
