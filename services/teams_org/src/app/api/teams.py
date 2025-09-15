from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.teams import TeamCreate, TeamRead, TeamUpdate
from app.services.deps import team_service_dep
from app.services.teams import TeamService
from app.models.teams import Team
from app.auth.deps import get_current_principal
from app.models.companies import Company

teams_router = APIRouter(tags=["teams"])


@teams_router.get("/companies/{company_id}/teams/{teams_id}", response_model=TeamRead)
async def get_team(
    team: TeamRead = Depends(), svc: TeamService = Depends(team_service_dep)
) -> Company:
    team_data = await svc.get(team.id)
    if not team_data:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_data


@teams_router.post(
    "/companies/{company_id}/teams/", response_model=TeamRead, status_code=201
)
async def create_team(
    company_id: UUID,
    team: TeamCreate,
    svc: TeamService = Depends(team_service_dep),
    principal=Depends(get_current_principal),
) -> Team:
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to create team")

    new_team = await svc.create(
        company_id=company_id,
        name=team.name,
        owner_user_id=team.owner_user_id,
    )
    return new_team


@teams_router.patch(
    "/teams/{team_id}/rename", response_model=TeamRead, status_code=status.HTTP_200_OK
)
async def rename_team(
    team_id: UUID,
    new_name: TeamUpdate,
    svc: TeamService = Depends(team_service_dep),
    principal=Depends(get_current_principal),
):
    team = await svc.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to rename team")
    updated_team = await svc.rename(team_id=team_id, new_name=new_name)  # type: ignore
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated_team
