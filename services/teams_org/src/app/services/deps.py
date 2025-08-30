from fastapi import Depends
from app.repositories.deps import company_repo_dep, team_repo_dep, membership_repo_dep
from app.repositories.companies import CompanyRepository
from app.repositories.memberships import MembershipRepository
from app.repositories.teams import TeamRepository
from app.services.companies import CompanyService
from app.services.memberships import MembershipService
from app.services.teams import TeamService


async def company_service_dep(
    companies: CompanyRepository = Depends(company_repo_dep),
    teams: TeamRepository = Depends(team_repo_dep),
) -> CompanyService:
    return CompanyService(companies=companies, teams=teams)

async def team_service_dep(
    companies: CompanyRepository = Depends(company_repo_dep),
    teams: TeamRepository = Depends(team_repo_dep),
    memberships: MembershipRepository = Depends(membership_repo_dep),
) -> TeamService:
    return TeamService(companies=companies, teams=teams, memberships=memberships)

async def membership_service_dep(
    teams: TeamRepository = Depends(team_repo_dep),
    memberships: MembershipRepository = Depends(membership_repo_dep),
) -> MembershipService:
    return MembershipService(teams=teams, memberships=memberships)
