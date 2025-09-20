import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import get_current_principal
from app.models.teams import Team
from app.schemas.teams import TeamCreate, TeamRead, TeamUpdate
from app.services.deps import team_service_dep
from app.services.teams import TeamService

teams_router = APIRouter(tags=["teams"])


@teams_router.get("/{teams_id}", response_model=TeamRead)
async def get_team(
    company_id: uuid.UUID,
    team_id: uuid.UUID,
    svc: TeamService = Depends(team_service_dep),
) -> Team:
    company = await svc.get_company(id_=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found for given ID")
    team = await svc.get_team(id_=team_id)
    if not team or team.company_id != company_id:
        raise HTTPException(status_code=404, detail="Team not found for given ID")
    return team


@teams_router.post("/", response_model=TeamRead, status_code=201)
async def create_team(
    company_id: uuid.UUID,
    team: TeamCreate,
    svc: TeamService = Depends(team_service_dep),
    principal=Depends(get_current_principal),
) -> Team:
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to create team")

    try:
        new_team = await svc.create(
            company_id=company_id,
            name=team.name,
            owner_user_id=team.owner_user_id,
        )
        return new_team
    except Exception as e:
        raise HTTPException(status_code=404, detail="Company not found")


@teams_router.patch(
    "/{team_id}/rename", response_model=TeamRead, status_code=status.HTTP_200_OK
)
async def rename_team(
    team_id: uuid.UUID,
    new_name: TeamUpdate,
    svc: TeamService = Depends(team_service_dep),
    principal=Depends(get_current_principal),
):
    team = await svc.get_team(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to rename team")
    updated_team = await svc.rename(team_id=team_id, new_name=new_name)  # type: ignore
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated_team
