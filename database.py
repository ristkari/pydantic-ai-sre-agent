from dataclasses import dataclass
from typing import Any

@dataclass
class Incident:
    id: int
    title: str
    description: str
    metrics: dict[str, Any]

# Mock database
INCIDENTS = {
    1: Incident(id=1, title="System has somewhat constrained CPU resources", description="Underlying K8S cluster is running low on CPU resource and average CPU load has increased beyond normal level", metrics={"CPU": 56, "MEMORY_PRESSURE": 10, "DISK_PRESSURE": 10}),
    2: Incident(id=2, title="Cloud provider outage", description="Cloud provider region failure. Unable to provision more capacity. Lost 2/3 of existing capacity.", metrics={"CPU": 90, "MEMORY_PRESSURE": 90, "DISK_PRESSURE": 90}),
}

class DatasourceConnection:
    async def incident_title(self, id: int) -> str:
        incident = INCIDENTS.get(id)
        return incident.title if incident else "Unknown Incident"

    async def incident_description(self, id: int) -> str:
        incident = INCIDENTS.get(id)
        return incident.description if incident else "Unknown Incident - No Description"

    async def incident_metrics(self, id: int) -> dict[str, Any]:
        incident = INCIDENTS.get(id)
        return incident.metrics if incident else {"CPU": 0, "MEMORY_PRESSURE": 0, "DISK_PRESSURE": 0, }

