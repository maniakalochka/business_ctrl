from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.repositories.companies import CompanyRepository
from app.repositories.memberships import MembershipRepository
from app.repositories.teams import TeamRepository

async def company_repo_dep(session: AsyncSession = Depends(get_async_session)) -> CompanyRepository:
    return CompanyRepository(session)

async def team_repo_dep(session: AsyncSession = Depends(get_async_session)) -> TeamRepository:
    return TeamRepository(session)

async def membership_repo_dep(session: AsyncSession = Depends(get_async_session)) -> MembershipRepository:
    return MembershipRepository(session)
