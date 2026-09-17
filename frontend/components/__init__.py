"""
Frontend interactive components: charts and observability inspector.
"""
from .charts import render_soil_health_chart, render_biodiversity_indicators, render_relationship_graph
from .debug_panel import render_debug_observability_panel

__all__ = [
    "render_soil_health_chart",
    "render_biodiversity_indicators",
    "render_relationship_graph",
    "render_debug_observability_panel"
]
