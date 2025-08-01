"""Service or use case for managing accounts."""

from app.entities.errors.accounts import (
    AccountNotFoundError as EntityAccountNotFoundError,
)
from app.entities.errors.accounts import (
    MonthYearNotFoundError as EntityMonthYearNotFoundError,
)
from app.entities.repositories.accounts import AccountRepositoryInterface
from app.use_cases.dto.accounts import AccountNameDTO, MonthLiteral, MonthYearDTO
from app.use_cases.errors.accounts import (
    AccountNotFoundError,
    AccountWithNameNotFoundError,
    MonthYearNotFoundError,
    MonthYearWithDetailsNotFoundError,
)
from app.use_cases.mappers.accounts import AccountNameMapper, MonthYearMapper


class AccountService:
    """Account service to handle business logic."""

    def __init__(self, account_repository: AccountRepositoryInterface):
        """Initialize the account service with the repository."""
        self.account_repository = account_repository

    async def get_or_create_account(self, account_name: str) -> AccountNameDTO:
        """Retrieve an existing account or create a new one with the provided name."""
        account_name_entity = await self.account_repository.get_or_create_account(account_name=account_name)

        return AccountNameMapper.to_dto(account_name_entity)

    async def get_account_by_name(self, account_name: str) -> AccountNameDTO:
        """Retrieve an account by its name.

        Raises:
            AccountWithNameNotFoundError: If the account with the provided name does not exist.
        """
        account_name_entity = await self.account_repository.get_account_by_name(account_name=account_name)

        if not account_name_entity:
            raise AccountWithNameNotFoundError(account_name=account_name)

        return AccountNameMapper.to_dto(account_name_entity)

    async def get_account_by_id(self, account_id: str) -> AccountNameDTO:
        """Retrieve an account by its ID.

        Raises:
            AccountNotFoundError: If the account with the provided ID does not exist.
        """
        account_name_entity = await self.account_repository.get_account_by_id(account_id=account_id)

        if not account_name_entity:
            raise AccountNotFoundError(account_id=account_id)

        return AccountNameMapper.to_dto(account_name_entity)

    async def get_all_accounts(self) -> list[AccountNameDTO]:
        """Retrieve all accounts."""
        account_name_entities = await self.account_repository.get_all_accounts()

        if not account_name_entities:
            return []

        return [AccountNameMapper.to_dto(account_name_entity) for account_name_entity in account_name_entities]

    async def update_account_name(self, account_id: str, account_name: str) -> AccountNameDTO:
        """Update an existing account name with the provided data.

        Raises:
            AccountNotFoundError: If the account with the provided ID does not exist.
        """
        try:
            account_name_entity = await self.account_repository.update_account_name(
                account_id=account_id, account_name=account_name
            )
        except EntityAccountNotFoundError as error:
            raise AccountNotFoundError(account_id=error.account_id) from error

        return AccountNameMapper.to_dto(account_name_entity)

    async def delete_account(self, account_id: str) -> None:
        """Delete an account by its ID.

        Raises:
            AccountNotFoundError: If the account with the provided ID does not exist.
        """
        try:
            await self.account_repository.delete_account(account_id=account_id)
        except EntityAccountNotFoundError as error:
            raise AccountNotFoundError(account_id=error.account_id) from error

    async def get_or_create_month_year(self, month: MonthLiteral, year: int) -> MonthYearDTO:
        """Retrieve an existing MonthYear or create a new one with the provided month and year."""
        month_year_entity = await self.account_repository.get_or_create_month_year(month=month, year=year)

        return MonthYearMapper.to_dto(month_year_entity)

    async def get_month_year_by_value(self, month: MonthLiteral, year: int) -> MonthYearDTO | None:
        """Retrieve a MonthYear by its month and year.

        Raises:
            MonthYearWithDetailsNotFoundError: If the MonthYear with the provided month and year does not exist.
        """
        month_year_entity = await self.account_repository.get_month_year_by_value(month=month, year=year)

        if not month_year_entity:
            raise MonthYearWithDetailsNotFoundError(month=month, year=year)

        return MonthYearMapper.to_dto(month_year_entity)

    async def get_month_year_by_id(self, month_year_id: str) -> MonthYearDTO | None:
        """Retrieve a MonthYear by its ID.

        Raises:
            MonthYearNotFoundError: If the MonthYear with the provided ID does not exist.
        """
        month_year_entity = await self.account_repository.get_month_year_by_id(month_year_id=month_year_id)

        if not month_year_entity:
            raise MonthYearNotFoundError(month_year_id=month_year_id)

        return MonthYearMapper.to_dto(month_year_entity) if month_year_entity else None

    async def get_all_month_years(self) -> list[MonthYearDTO]:
        """Retrieve all MonthYears."""
        month_year_entities = await self.account_repository.get_all_month_years()

        if not month_year_entities:
            return []

        return [MonthYearMapper.to_dto(month_year_entity) for month_year_entity in month_year_entities]

    async def update_month_year(self, month_year_id: str, month: MonthLiteral, year: int) -> MonthYearDTO:
        """Update an existing MonthYear with the provided data.

        Raises:
            MonthYearNotFoundError: If the MonthYear with the provided ID does not exist.
        """
        try:
            month_year_entity = await self.account_repository.update_month_year(
                month_year_id=month_year_id, month=month, year=year
            )
        except EntityMonthYearNotFoundError as error:
            raise MonthYearNotFoundError(month_year_id=error.month_year_id) from error

        return MonthYearMapper.to_dto(month_year_entity)

    async def delete_month_year(self, month_year_id: str) -> None:
        """Delete a MonthYear by its ID.

        Raises:
            MonthYearNotFoundError: If the MonthYear with the provided ID does not exist.
        """
        try:
            await self.account_repository.delete_month_year(month_year_id=month_year_id)
        except EntityMonthYearNotFoundError as error:
            raise MonthYearNotFoundError(month_year_id=error.month_year_id) from error
