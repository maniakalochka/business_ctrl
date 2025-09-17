from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import get_current_principal
from app.models.teams import Team
from app.schemas.teams import TeamCreate, TeamRead, TeamUpdate
from app.services.deps import team_service_dep
from app.services.teams import TeamService

teams_router = APIRouter(tags=["teams"])


@teams_router.get("/{team_name}", response_model=TeamRead)
async def get_team(
        team_name: str,
        svc: TeamService = Depends(team_service_dep),
        principal=Depends(get_current_principal),
) -> TeamRead:
    if not principal.role in {"admin", "manager"}:
        raise HTTPException(status_code=403, detail="Not authorized to get team")
    team = await svc.get_by_name(name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


# FIX: always return empty list
@teams_router.get("/", response_model=list[TeamRead])
async def list_teams(
        company_name: str,
        svc: TeamService = Depends(team_service_dep),
        principal=Depends(get_current_principal),
) -> list[Team]:
    if not principal.role in {"admin", "manager"}:
        raise HTTPException(status_code=403, detail="Not authorized to list teams")
    teams = await svc.list_by_company(company_name)
    return teams


@teams_router.post("/", response_model=TeamRead, status_code=201)
async def create_team(
        company_name: str,
        team: TeamCreate,
        svc: TeamService = Depends(team_service_dep),
        principal=Depends(get_current_principal),
) -> TeamRead:
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to create team")
    from app.exceptions.exceptions import AlreadyExists

    try:
        new_team = await svc.create(
            company_name=company_name,
            name=team.name,
            owner_user_id=team.owner_user_id,
        )
    except AlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    return new_team


@teams_router.patch(
    "{team_id}/rename", response_model=TeamRead, status_code=status.HTTP_200_OK
)
async def rename_team(
        team_id: UUID,
        new_name: TeamUpdate,
        svc: TeamService = Depends(team_service_dep),
        principal=Depends(get_current_principal),
) -> TeamRead:
    from app.exceptions.exceptions import AlreadyExists

    try:
        team = await svc.get(team_id)
    except AlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Not authorized to rename team")
    updated_team = await svc.rename(team_id=team_id, new_name=new_name)  # type: ignore
    return updated_team
