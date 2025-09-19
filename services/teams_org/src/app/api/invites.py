import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import get_current_principal
from app.schemas.invites import InviteCreateRequest, InviteRead, InviteAcceptRequest
from app.schemas.principal import Principal
from app.services.deps import token_service_dep
from app.services.invites import InvitesService

inv_router = APIRouter(tags=["invites"])


@inv_router.post(
    "/",
    response_model=InviteRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_invite(
    team_id: uuid.UUID,
    data: InviteCreateRequest,
    principal: Principal = Depends(get_current_principal),
    svc: InvitesService = Depends(token_service_dep),
) -> InviteRead:
    if principal.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    team_id = data.team_id
    try:
        invite = await svc.create_invite(
            team_id=team_id,
            email=data.email,
            inviter_id=principal.sub,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return InviteRead.model_validate(invite)


@inv_router.post("/{invite_id}/accept", response_model=InviteRead)
async def accept_invite(
    team_id: uuid.UUID,
    invite_id: uuid.UUID,
    data: InviteAcceptRequest,
    principal: Principal = Depends(get_current_principal),
    svc: InvitesService = Depends(token_service_dep),
) -> InviteRead:
    try:
        invite = await svc.accept_invite(token=data.token, user_id=principal.sub)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return InviteRead.model_validate(invite)
