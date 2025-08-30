from fastapi import APIRouter, Depends, HTTPException
from app.schemas.teams import TeamRead, TeamCreate
from app.services.teams import TeamService
from app.services.deps import team_service_dep

teams_router = APIRouter(prefix="/teams", tags=["teams"])

@teams_router.get("/{team_id}")
async def get_team(
    team: TeamRead = Depends(),
    svc: TeamService = Depends(team_service_dep)
):
    team_data = await svc.get(team.id)
    if not team_data:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_data

@teams_router.post("/")
async def create_team(
    team: TeamCreate,
    svc: TeamService = Depends(team_service_dep)
):
    team_data = await svc.create(
        company_id=team.companies_id,
        name=team.name,
        owner_user_id=team.owner_user_id
    )
