# import uuid
# from fastapi import APIRouter, Depends

# from app.security.service_token import verify_service_token


# mbs_router = APIRouter()


# @mbs_router.get("/memberships/{org_id}/users/{user_id}/role")
# async def get_membership_role(
#     org_id: uuid.UUID,
#     email: str,
#     token: str = Depends(verify_service_token)

# ):
