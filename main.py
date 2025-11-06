import asyncio
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from database import DatasourceConnection
from incident_dependencies import IncidentDependencies

_ = load_dotenv()

class IncidentOutput(BaseModel):
    response_text: str = Field(description="Description of the incident status")
    degradation: bool = Field(description="Is production service degraded")
    emergency: bool = Field(description="Is there production outage")
    criticality: int = Field(description="Criticality level", ge=0, le=5)


incident_agent = Agent(
    "gemini-2.5-pro",
    deps_type=IncidentDependencies,
    output_type=IncidentOutput,
    system_prompt=(
        "You are SRE engineer. Your task is to provide analysis of the incident reports based on the metrics."
        "Provide clear and concise advice, evaluate possible effect to production and assess urgency."
    ),
)


@incident_agent.system_prompt
async def add_incident_title(ctx: RunContext[IncidentDependencies]) -> str:
    incident_title = await ctx.deps.db.incident_title(id=ctx.deps.incident_id)
    return f"Incident title: {incident_title!r}."

@incident_agent.system_prompt
async def add_incident_description(ctx: RunContext[IncidentDependencies]) -> str:
    incident_description = await ctx.deps.db.incident_description(id=ctx.deps.incident_id)
    return f"Incident description: {incident_description!r}."

@incident_agent.tool
async def incident_metrics(ctx: RunContext[IncidentDependencies]) -> dict[str, Any]:
    """Returns latest metrics for the incident"""
    return await ctx.deps.db.incident_metrics(id=ctx.deps.incident_id)


async def main() -> None:
    deps = IncidentDependencies(incident_id=2, db=DatasourceConnection())

    result = await incident_agent.run(
        # "System is giving errors and is not responding to my requests.",
        "There is sudden increase in support requests. What is going on with the system?",
        deps=deps,
    )
    print(result.output)
    """
    Example result:
    response_text='There is major incident, operations team is working on it and relevant people are informed.'
    degradation=True
    emergency=True
    criticality=5
    """

if __name__ == "__main__":
    asyncio.run(main())
