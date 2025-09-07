from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.teams import TeamCreate, TeamRead
from app.services.deps import team_service_dep
from app.services.teams import TeamService
from services.teams_org.src.app.models.teams import Team

teams_router = APIRouter(prefix="/teams", tags=["teams"])


@teams_router.get("/{team_id}")
async def get_team(
    team: TeamRead = Depends(), svc: TeamService = Depends(team_service_dep)
):
    team_data = await svc.get(team.id)
    if not team_data:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_data


@teams_router.post("/", response_model=TeamRead, status_code=201)
async def create_team(
    team: TeamCreate, svc: TeamService = Depends(team_service_dep)
) -> Team:
    teams = await svc.create(
        company_id=team.companies_id, name=team.name, owner_user_id=team.owner_user_id
    )
    return teams


@teams_router.patch("/{team_id}/rename", response_model=TeamRead, status_code=204)
async def rename_team(
    team_id: UUID, new_name: str, svc: TeamService = Depends(team_service_dep)
) -> None:
    await svc.rename(team_id=team_id, new_name=new_name)
