from uuid import uuid4
import pytest

from app.exceptions.exceptions import NotFound


@pytest.mark.asyncio
class TestTeamService:
    async def test_create_team_success(self, service):
        company_id = uuid4()
        name = "Test Team"
        lead_user_id = uuid4()

        service._companies.get.return_value = {"id": company_id}
        service._teams.create_team_atomic.return_value = {"id": uuid4(), "name": name}

        result = await service.create(company_id=company_id, name=name, lead_user_id=lead_user_id)

        service._companies.get.assert_awaited_once_with(company_id)
        service._teams.create_team_atomic.assert_awaited_once_with(
            company_id=company_id, name=name, lead_user_id=lead_user_id
        )
        assert result["name"] == name

    async def test_create_team_not_found(self, service):
        company_id = uuid4()
        name = "Test Team"

        service._companies.get.return_value = None

        with pytest.raises(NotFound, match="Компания не найдена"):
            await service.create(company_id=company_id, name=name)

        service._companies.get.assert_awaited_once_with(company_id)

    async def test_rename_team_success(self, service):
        team_id = uuid4()
        new_name = "Renamed Team"

        service._teams.get.return_value = {"id": team_id}

        await service.rename(team_id=team_id, new_name=new_name)

        service._teams.get.assert_awaited_once_with(team_id)
        service._teams.rename_atomic.assert_awaited_once_with(team_id=team_id, new_name=new_name)

    async def test_rename_team_not_found(self, service):
        team_id = uuid4()
        new_name = "Renamed Team"

        service._teams.get.return_value = None

        with pytest.raises(NotFound, match="Команда не найдена"):
            await service.rename(team_id=team_id, new_name=new_name)

        service._teams.get.assert_awaited_once_with(team_id)

    async def test_archive_team_success(self, service):
        team_id = uuid4()

        service._teams.get.return_value = {"id": team_id}

        await service.archive(team_id=team_id)

        service._teams.get.assert_awaited_once_with(team_id)
        service._memberships.archive_team_if_empty_atomic.assert_awaited_once_with(team_id)

    async def test_archive_team_not_found(self, service):
        team_id = uuid4()

        service._teams.get.return_value = None

        with pytest.raises(NotFound, match="Команда не найдена"):
            await service.archive(team_id=team_id)

        service._teams.get.assert_awaited_once_with(team_id)

    async def test_list_by_company_success(self, service):
        company_id = uuid4()
        only_active = True
        limit = 10
        offset = 0

        service._companies.get.return_value = {"id": company_id}
        service._teams.list_by_company.return_value = [{"id": uuid4(), "name": "Team 1"}]

        result = await service.list_by_company(company_id=company_id, only_active=only_active, limit=limit, offset=offset)

        service._companies.get.assert_awaited_once_with(company_id)
        service._teams.list_by_company.assert_awaited_once_with(
            company_id, only_active=only_active, limit=limit, offset=offset
        )
        assert len(result) == 1

    async def test_list_by_company_not_found(self, service):
        company_id = uuid4()

        service._companies.get.return_value = None

        with pytest.raises(NotFound, match="Компания не найдена"):
            await service.list_by_company(company_id=company_id)

        service._companies.get.assert_awaited_once_with(company_id)
