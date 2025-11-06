from dataclasses import dataclass

from database import DatasourceConnection


@dataclass
class IncidentDependencies:
    incident_id: int
    db: DatasourceConnection
