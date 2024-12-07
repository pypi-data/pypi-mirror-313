# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from functools import reduce
from typing import Any, Dict, List, Optional
from uuid import UUID

from sql import Column, Flavor, Table
from sql.conditionals import Case
from sql.operators import And, Equal, NotEqual

from tikka.adapters.repository.categories import TABLE_NAME as CATEGORIES_TABLE_NAME
from tikka.adapters.repository.identities import TABLE_NAME as IDENTITIES_TABLE_NAME
from tikka.adapters.repository.sqlite3 import Sqlite3RepositoryInterface
from tikka.adapters.repository.wallets import TABLE_NAME as WALLETS_TABLE_NAME
from tikka.domains.entities.account import Account
from tikka.interfaces.adapters.repository.accounts import AccountsRepositoryInterface

TABLE_NAME = "accounts"

# config sql with ? as param style
Flavor.set(Flavor(paramstyle="qmark"))
# create sql table wrapper
sql_accounts_table = Table(TABLE_NAME)

CATEGORIES_TABLE_NB_COLUMNS = 4
CATEGORY_NAME_ALIAS_COLUMN = "category_name_alias"
CATEGORY_ID_ALIAS_COLUMN = "category_id_alias"


class Sqlite3AccountsRepository(
    AccountsRepositoryInterface, Sqlite3RepositoryInterface
):
    """
    Sqlite3AccountsRepository class
    """

    def list(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_column: Optional[str] = None,
        sort_order: str = AccountsRepositoryInterface.SORT_ORDER_ASCENDING,
    ) -> List[Account]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.list.__doc__
        )

        sql_columns = {
            AccountsRepositoryInterface.COLUMN_ADDRESS: sql_accounts_table.address,
            AccountsRepositoryInterface.COLUMN_NAME: sql_accounts_table.name,
            AccountsRepositoryInterface.COLUMN_CRYPTO_TYPE: sql_accounts_table.crypto_type,
            AccountsRepositoryInterface.COLUMN_BALANCE: sql_accounts_table.balance,
            AccountsRepositoryInterface.COLUMN_PATH: sql_accounts_table.path,
            AccountsRepositoryInterface.COLUMN_ROOT: sql_accounts_table.root,
            AccountsRepositoryInterface.COLUMN_FILE_IMPORT: sql_accounts_table.file_import,
            AccountsRepositoryInterface.COLUMN_CATEGORY_ID: sql_accounts_table.category_id,
        }

        # if sort column...
        if sort_column is not None:
            # set sort column
            sql_sort_colum = Column(sql_accounts_table, sort_column)
            # create select query wrapper with order by
            sql_select = sql_accounts_table.select(
                order_by=sql_sort_colum.asc
                if sort_order == AccountsRepositoryInterface.SORT_ORDER_ASCENDING
                else sql_sort_colum.desc,
            )
        else:
            #  create select query wrapper without order by
            sql_select = sql_accounts_table.select()

        # create where conditions
        conditions = []
        if filters is not None:
            for key, value in filters.items():
                if key == AccountsRepositoryInterface.COLUMN_ROOT:
                    if value is True:
                        conditions.append(Equal(sql_accounts_table.root, None))
                    elif value is False:
                        conditions.append(NotEqual(sql_accounts_table.root, None))
                    elif isinstance(value, str):
                        conditions.append(
                            sql_accounts_table.root
                            == filters[AccountsRepositoryInterface.COLUMN_ROOT]
                        )
                else:
                    conditions.append(sql_columns[key] == value)

        # conditions are added with and operator
        def and_(a, b):
            return And((a, b))

        if len(conditions) > 0:
            sql_select.where = reduce(and_, conditions)

        sql, args = tuple(sql_select)
        result_set = self.client.select(sql, args)

        list_ = []
        for row in result_set:
            list_.append(get_account_from_row(row))

        return list_

    def table_view(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_column_index: Optional[int] = None,
        sort_order: str = AccountsRepositoryInterface.SORT_ORDER_ASCENDING,
    ) -> List[AccountsRepositoryInterface.TableViewRow]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.table_view.__doc__
        )
        # we need to get the category of root account for derived account
        # in order to do that, we join :
        # - the category table for root accounts
        # - the account table to get root account of derived accounts
        # - the category table for the joined account table to category of the root account of derived accounts

        # we also need to sort/filter by wallet column (stored or not)
        # in order to do that, we join :
        # - the wallet table

        # SELECT "e"."address", "a"."identity_index", "a"."balance", "a"."name", "a"."address", "a"."path", "a"."root",
        # "a"."crypto_type",
        # CASE WHEN ("a"."root" IS NULL) THEN "b"."name" ELSE "d"."name" END AS "category_name_alias",
        # CASE WHEN ("a"."root" IS NULL) THEN "b"."id" ELSE "d"."id" END AS "category_id_alias"
        # FROM "accounts" AS "a"
        # LEFT JOIN "categories" AS "b" ON (("a"."root" IS NULL) AND ("b"."id" = "a"."category_id"))
        # LEFT JOIN "accounts" AS "c" ON (("c"."root" IS NULL) AND ("c"."address" = "a"."root"))
        # LEFT JOIN "categories" AS "d" ON ("d"."id" = "c"."category_id")
        # LEFT JOIN "wallets" AS "e" ON ("e"."address" = "a"."address")

        # join the category table for root accounts
        sql_categories_join = sql_accounts_table.join(
            Table(CATEGORIES_TABLE_NAME), "LEFT"
        )
        sql_categories_join.condition = Equal(sql_accounts_table.root, None) & (
            sql_categories_join.right.id == sql_accounts_table.category_id
        )
        # join the account table to get root accounts of derived accounts
        sql_accounts_join = sql_categories_join.join(Table(TABLE_NAME), "LEFT")
        sql_accounts_join.condition = Equal(sql_accounts_join.right.root, None) & (
            sql_accounts_join.right.address == sql_accounts_table.root
        )
        # join the category table for root account of derived accounts
        sql_categories_join2 = sql_accounts_join.join(
            Table(CATEGORIES_TABLE_NAME), "LEFT"
        )
        sql_categories_join2.condition = (
            sql_categories_join2.right.id == sql_accounts_join.right.category_id
        )
        # join wallet table to get wallet
        sql_wallets_join = sql_categories_join2.join(Table(WALLETS_TABLE_NAME), "LEFT")
        sql_wallets_join.condition = (
            sql_wallets_join.right.address == sql_accounts_table.address
        )
        sql_identities_join = sql_wallets_join.join(
            Table(IDENTITIES_TABLE_NAME), "LEFT"
        )
        sql_identities_join.condition = (
            sql_identities_join.right.address == sql_accounts_table.address
        )
        # create select query wrapper
        sql_select = sql_identities_join.select(
            sql_wallets_join.right.address,
            sql_identities_join.right.index_,
            sql_accounts_table.balance,
            sql_accounts_table.name,
            sql_accounts_table.address,
            sql_accounts_table.path,
            sql_accounts_table.root,
            sql_accounts_table.crypto_type,
            Case(
                (Equal(sql_accounts_table.root, None), sql_categories_join.right.name),
                else_=sql_categories_join2.right.name,
            ).as_(CATEGORY_NAME_ALIAS_COLUMN),
            # add category_id column for category_id filter
            Case(
                (Equal(sql_accounts_table.root, None), sql_categories_join.right.id),
                else_=sql_categories_join2.right.id,
            ).as_(CATEGORY_ID_ALIAS_COLUMN),
        )

        sql_sort_columns = [
            sql_wallets_join.right.address,
            sql_identities_join.right.index_,
            sql_accounts_table.balance,
            sql_accounts_table.name,
            sql_accounts_table.address,
            sql_accounts_table.path,
            sql_accounts_table.root,
            sql_accounts_table.crypto_type,
            sql_accounts_table.category_id.as_(CATEGORY_NAME_ALIAS_COLUMN),
        ]

        # if sort column...
        if sort_column_index is not None:
            # set sort column by its index
            sql_sort_column = sql_sort_columns[sort_column_index]
            if sql_sort_column is not None:
                sql_select.order_by = (
                    sql_sort_column.asc
                    if sort_order == AccountsRepositoryInterface.SORT_ORDER_ASCENDING
                    else sql_sort_column.desc
                )

        sql_filter_columns = {
            AccountsRepositoryInterface.TABLE_VIEW_FILTER_BY_CATEGORY_ID: sql_accounts_table.category_id.as_(
                CATEGORY_ID_ALIAS_COLUMN
            ),
            AccountsRepositoryInterface.TABLE_VIEW_FILTER_BY_WALLET: sql_wallets_join.right.address,
        }

        # create where conditions
        conditions = []
        if filters is not None:
            for key, value in filters.items():
                if key not in sql_filter_columns:
                    continue
                if key == AccountsRepositoryInterface.TABLE_VIEW_FILTER_BY_WALLET:
                    if value is True:
                        conditions.append(NotEqual(sql_filter_columns[key], None))
                    elif value is False:
                        conditions.append(Equal(sql_filter_columns[key], None))
                else:
                    conditions.append(sql_filter_columns[key] == value)

        # conditions are added with and operator
        def and_(a, b):
            return And((a, b))

        if len(conditions) > 0:
            sql_select.where = reduce(and_, conditions)

        sql, args = tuple(sql_select)
        result_set = self.client.select(sql, args)

        list_ = []
        for row in result_set:
            table_view_row = AccountsRepositoryInterface.TableViewRow(
                *row[
                    : len(
                        AccountsRepositoryInterface.TableViewRow.__dataclass_fields__  # type: ignore
                    )
                ],
            )
            list_.append(table_view_row)
        return list_

    def add(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.add.__doc__
        )

        # insert only non hidden fields
        self.client.insert(
            TABLE_NAME,
            **get_fields_from_account(account),
        )

    def update(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.update.__doc__
        )

        # update only non hidden fields
        self.client.update(
            TABLE_NAME,
            f"address='{account.address}'",
            **get_fields_from_account(account),
        )

    def delete(self, account: Account) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.delete.__doc__
        )

        self.client.delete(TABLE_NAME, address=account.address)

    def count(self) -> int:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            AccountsRepositoryInterface.count.__doc__
        )
        row = self.client.select_one(f"SELECT count(address) FROM {TABLE_NAME}")
        if row is None:
            return 0

        return row[0]


def get_fields_from_account(account: Account) -> dict:
    """
    Return a dict of supported fields with normalized value

    :param account: Account instance
    :return:
    """
    fields = {}
    for (key, value) in account.__dict__.items():
        if key.startswith("_"):
            continue
        if isinstance(value, UUID):
            value = value.hex
        fields[key] = value

    return fields


def get_account_from_row(row: tuple) -> Account:
    """
    Return an Account instance from a result set row

    :param row: Result set row
    :return:
    """
    values: List[Any] = []
    count = 0
    for value in row:
        if count == 7 and value is not None:
            values.append(UUID(hex=value))
        elif count == 6:
            values.append(bool(value))
        else:
            values.append(value)
        count += 1

    return Account(*values)  # pylint: disable=no-value-for-parameter
