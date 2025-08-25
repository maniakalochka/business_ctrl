import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.teams import Team
from app.models.users import User
from app.repositories import UserRepository

pytestmark = pytest.mark.asyncio

async def _mk_team(session: AsyncSession, name="Alpha", slug="alpha") -> Team:
    t = Team(id=uuid.uuid4(), name=name, slug=slug)
    session.add(t)
    await session.commit()
    await session.refresh(t)
    return t

async def _mk_user(session: AsyncSession, **kwargs) -> User:
    """
    Создаёт пользователя напрямую через ORM.
    Минимально требуемые поля: email, hashed_password, role.
    Остальные — опциональны.
    """
    defaults = dict(
        email="user@example.com",
        hashed_password="hashed",
        is_active=True,
        is_superuser=False,
        is_verified=True,
        role="employee",
        first_name=None,
        last_name=None,
        phone=None,
        team_id=None,
        supervisor_id=None,
    )
    defaults.update(kwargs)
    u = User(**defaults)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u

async def test_by_email_found(session: AsyncSession):
    repo = UserRepository(session)
    await _mk_user(session, email="a@b.com")
    got = await repo.by_email("a@b.com")
    assert got is not None
    assert got.email == "a@b.com"

async def test_by_email_not_found(session: AsyncSession):
    repo = UserRepository(session)
    got = await repo.by_email("nope@example.com")
    assert got is None

# async def test_by_team(session: AsyncSession):
#     repo = UserRepository(session)
#     team = await _mk_team(session, name="Bravo", slug="bravo")
#     u1 = await _mk_user(session, email="t1@ex.com", team_id=team.id)
#     u2 = await _mk_user(session, email="t2@ex.com", team_id=team.id)
#     await _mk_user(session, email="other@ex.com", team_id=None)

#     res = await repo.by_team(team.id)
#     emails = sorted(u.email for u in res)
#     assert emails == ["t1@ex.com", "t2@ex.com"]

# async def test_subordinates_of(session: AsyncSession):
#     repo = UserRepository(session)
#     boss = await _mk_user(session, email="boss@ex.com", role="manager")
#     s1 = await _mk_user(session, email="s1@ex.com", supervisor_id=boss.id)
#     s2 = await _mk_user(session, email="s2@ex.com", supervisor_id=boss.id)
#     await _mk_user(session, email="other@ex.com")  # без начальника

#     subs = await repo.subordinates_of(boss.id)
#     emails = sorted(u.email for u in subs)
#     assert emails == ["s1@ex.com", "s2@ex.com"]

# async def test_managers(session: AsyncSession):
#     repo = UserRepository(session)
#     await _mk_user(session, email="m1@ex.com", role="manager")
#     await _mk_user(session, email="m2@ex.com", role="manager")
#     await _mk_user(session, email="e1@ex.com", role="employee")

#     res = await repo.managers()
#     emails = sorted(u.email for u in res)
#     assert emails == ["m1@ex.com", "m2@ex.com"]
