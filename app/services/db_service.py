import sqlite3
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.config import settings

class DBService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.SQLITE_DB_PATH
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize all required tables for environmental intelligence."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Environmental Observations Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS environmental_observations (
                id TEXT PRIMARY KEY,
                location_name TEXT,
                latitude REAL,
                longitude REAL,
                region TEXT,
                country TEXT,
                climate_zone TEXT,
                soil_ph REAL,
                soil_organic_carbon REAL,
                soil_moisture REAL,
                land_use TEXT,
                land_cover TEXT,
                monoculture_or_polyculture TEXT,
                habitat_diversity TEXT,
                habitat_fragmentation TEXT,
                species_richness TEXT,
                species_diversity TEXT,
                pollinator_presence TEXT,
                microbial_diversity TEXT,
                temperature REAL,
                rainfall TEXT,
                rainfall_variability TEXT,
                drought_condition TEXT,
                pollution_level TEXT,
                pesticide_intensity TEXT,
                deforestation_level TEXT,
                urbanization TEXT,
                land_disturbance TEXT,
                water_availability TEXT,
                irrigation TEXT,
                water_stress TEXT,
                raw_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Conversations & Session Memory Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accumulated_state TEXT,
                messages_history TEXT
            )
            """)

            # Scientific Sources Registry Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources_registry (
                document_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                organization TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                source_type TEXT NOT NULL,
                environmental_domain TEXT NOT NULL,
                variables TEXT NOT NULL,
                geographic_scope TEXT NOT NULL,
                citation TEXT NOT NULL,
                url TEXT NOT NULL,
                reliability_score REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Recommendations Audit Log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS recommendation_logs (
                id TEXT PRIMARY KEY,
                conversation_id TEXT,
                recommendation_title TEXT,
                interventions_json TEXT,
                variables_used TEXT,
                confidence TEXT,
                citations_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.commit()

    def save_observation(self, state: Dict[str, Any]) -> str:
        obs_id = state.get("id") or str(uuid.uuid4())
        state["id"] = obs_id
        with self.get_connection() as conn:
            cursor = conn.cursor()
            raw_json = json.dumps(state, default=str)
            cursor.execute("""
            INSERT OR REPLACE INTO environmental_observations (
                id, location_name, latitude, longitude, region, country, climate_zone,
                soil_ph, soil_organic_carbon, soil_moisture, land_use, land_cover,
                monoculture_or_polyculture, habitat_diversity, habitat_fragmentation,
                species_richness, species_diversity, pollinator_presence, microbial_diversity,
                temperature, rainfall, rainfall_variability, drought_condition,
                pollution_level, pesticide_intensity, deforestation_level, urbanization,
                land_disturbance, water_availability, irrigation, water_stress, raw_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                obs_id,
                state.get("location_name"),
                state.get("latitude"),
                state.get("longitude"),
                state.get("region"),
                state.get("country"),
                state.get("climate_zone"),
                state.get("soil_ph"),
                state.get("soil_organic_carbon"),
                state.get("soil_moisture"),
                state.get("land_use"),
                state.get("land_cover"),
                state.get("monoculture_or_polyculture"),
                str(state.get("habitat_diversity")) if state.get("habitat_diversity") is not None else None,
                str(state.get("habitat_fragmentation")) if state.get("habitat_fragmentation") is not None else None,
                str(state.get("species_richness")) if state.get("species_richness") is not None else None,
                str(state.get("species_diversity")) if state.get("species_diversity") is not None else None,
                str(state.get("pollinator_presence")) if state.get("pollinator_presence") is not None else None,
                str(state.get("microbial_diversity")) if state.get("microbial_diversity") is not None else None,
                state.get("temperature"),
                str(state.get("rainfall")) if state.get("rainfall") is not None else None,
                str(state.get("rainfall_variability")) if state.get("rainfall_variability") is not None else None,
                str(state.get("drought_condition")) if state.get("drought_condition") is not None else None,
                str(state.get("pollution_level")) if state.get("pollution_level") is not None else None,
                str(state.get("pesticide_intensity")) if state.get("pesticide_intensity") is not None else None,
                str(state.get("deforestation_level")) if state.get("deforestation_level") is not None else None,
                str(state.get("urbanization")) if state.get("urbanization") is not None else None,
                str(state.get("land_disturbance")) if state.get("land_disturbance") is not None else None,
                str(state.get("water_availability")) if state.get("water_availability") is not None else None,
                str(state.get("irrigation")) if state.get("irrigation") is not None else None,
                str(state.get("water_stress")) if state.get("water_stress") is not None else None,
                raw_json
            ))
            conn.commit()
        return obs_id

    def get_observation(self, obs_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM environmental_observations WHERE id = ?", (obs_id,))
            row = cursor.fetchone()
            if row:
                res = dict(row)
                if res.get("raw_json"):
                    try:
                        data = json.loads(res["raw_json"])
                        data["id"] = res["id"]
                        data["created_at"] = res.get("created_at")
                        return data
                    except Exception:
                        pass
                return res
        return None

    def get_all_observations(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM environmental_observations ORDER BY created_at DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM conversations WHERE conversation_id = ?", (conversation_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "conversation_id": row["conversation_id"],
                    "accumulated_state": json.loads(row["accumulated_state"]) if row["accumulated_state"] else {},
                    "messages_history": json.loads(row["messages_history"]) if row["messages_history"] else []
                }
        return None

    def save_conversation(self, conversation_id: str, accumulated_state: Dict[str, Any], messages: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO conversations (conversation_id, updated_at, accumulated_state, messages_history)
            VALUES (?, CURRENT_TIMESTAMP, ?, ?)
            """, (
                conversation_id,
                json.dumps(accumulated_state, default=str),
                json.dumps(messages, default=str)
            ))
            conn.commit()

    def register_source(self, source_doc: Dict[str, Any]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO sources_registry (
                document_id, title, organization, publication_year, source_type,
                environmental_domain, variables, geographic_scope, citation, url, reliability_score
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                source_doc["document_id"],
                source_doc["title"],
                source_doc["organization"],
                source_doc["publication_year"],
                source_doc["source_type"],
                source_doc["environmental_domain"],
                json.dumps(source_doc.get("variables", [])),
                source_doc["geographic_scope"],
                source_doc["citation"],
                source_doc["url"],
                source_doc.get("reliability_score", 0.95)
            ))
            conn.commit()

    def get_all_sources(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sources_registry ORDER BY organization, publication_year DESC")
            rows = cursor.fetchall()
            results = []
            for r in rows:
                d = dict(r)
                try:
                    d["variables"] = json.loads(d["variables"])
                except Exception:
                    pass
                results.append(d)
            return results

db_service = DBService()
