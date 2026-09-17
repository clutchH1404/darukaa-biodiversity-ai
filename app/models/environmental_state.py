from typing import Optional, Union, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone

class EnvironmentalState(BaseModel):
    """
    Comprehensive environmental observation state representing 6 key domains:
    Soil, Land, Biodiversity, Climate, Human Impact, Water, plus Spatial context.
    """
    # Identification & Location
    id: Optional[str] = None
    location_name: Optional[str] = Field(None, description="Descriptive location name")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    region: Optional[str] = Field(None, description="e.g., semi-arid, Mediterranean, tropical")
    country: Optional[str] = None
    climate_zone: Optional[str] = None

    # SOIL VARIABLES
    soil_ph: Optional[float] = Field(None, ge=0.0, le=14.0, description="Soil pH value (0-14)")
    soil_organic_carbon: Optional[float] = Field(None, ge=0.0, le=100.0, description="Soil organic carbon percentage (% SOC)")
    soil_moisture: Optional[float] = Field(None, ge=0.0, le=100.0, description="Volumetric or relative soil moisture %")

    # LAND VARIABLES
    land_use: Optional[str] = Field(None, description="e.g., monoculture wheat, agroforestry, pasture")
    land_cover: Optional[str] = Field(None, description="e.g., cropland, scrubland, forest, bare soil")
    monoculture_or_polyculture: Optional[str] = Field(None, description="'monoculture' or 'polyculture'")
    habitat_diversity: Optional[Union[float, str]] = Field(None, description="Index (0-1) or qualitative (low/medium/high)")
    habitat_fragmentation: Optional[Union[float, str]] = Field(None, description="Fragmentation level (low/medium/high or 0-1)")

    # BIODIVERSITY VARIABLES
    species_richness: Optional[Union[float, str]] = Field(None, description="Count or qualitative (low/medium/high)")
    species_diversity: Optional[Union[float, str]] = Field(None, description="Shannon index or qualitative rating")
    pollinator_presence: Optional[Union[float, str]] = Field(None, description="Abundance score or qualitative (low/medium/high)")
    microbial_diversity: Optional[Union[float, str]] = Field(None, description="Soil microbial activity/diversity rating")

    # CLIMATE VARIABLES
    temperature: Optional[float] = Field(None, description="Mean temperature in Celsius")
    rainfall: Optional[Union[float, str]] = Field(None, description="Annual rainfall in mm or qualitative (low/medium/high)")
    rainfall_variability: Optional[Union[float, str]] = Field(None, description="e.g., high, unpredictable, seasonal")
    drought_condition: Optional[Union[bool, str]] = Field(None, description="Current drought status")

    # HUMAN IMPACT VARIABLES
    pollution_level: Optional[Union[float, str]] = Field(None, description="Pollution level (low/moderate/severe)")
    pesticide_intensity: Optional[Union[float, str]] = Field(None, description="Pesticide application intensity")
    deforestation_level: Optional[Union[float, str]] = Field(None, description="Deforestation impact")
    urbanization: Optional[Union[float, str]] = Field(None, description="Proximity to urban sprawl")
    land_disturbance: Optional[Union[float, str]] = Field(None, description="Tillage or physical disturbance level")

    # WATER VARIABLES
    water_availability: Optional[Union[float, str]] = Field(None, description="Water access rating")
    irrigation: Optional[Union[bool, str]] = Field(None, description="Irrigation infrastructure present")
    water_stress: Optional[Union[float, str]] = Field(None, description="Hydrological stress index or level")

    timestamp: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("soil_ph", mode="before")
    def parse_ph(cls, v):
        if v is None or v == "":
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    @field_validator("soil_organic_carbon", mode="before")
    def parse_soc(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str) and "%" in v:
            v = v.replace("%", "").strip()
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    @field_validator("soil_moisture", mode="before")
    def parse_moisture(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, str) and "%" in v:
            v = v.replace("%", "").strip()
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    def get_known_variables(self) -> Dict[str, Any]:
        """Returns all non-null environmental variables."""
        return {
            k: v for k, v in self.model_dump().items()
            if v is not None and k not in ("id", "timestamp")
        }

    def count_known_variables(self) -> int:
        """Count how many environmental parameters are provided."""
        return len(self.get_known_variables())

class EnvironmentalObservationCreate(EnvironmentalState):
    pass

class EnvironmentalObservationResponse(EnvironmentalState):
    id: str
    created_at: Optional[Union[datetime, str]] = None
