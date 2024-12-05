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

from dataclasses import dataclass
from typing import Optional, TypeVar
from uuid import UUID

AccountType = TypeVar("AccountType", bound="Account")


@dataclass
class Account:

    address: str
    name: Optional[str] = None
    crypto_type: Optional[int] = None
    balance: Optional[int] = None
    path: Optional[str] = None
    root: Optional[str] = None
    file_import: bool = False
    category_id: Optional[UUID] = None

    def __str__(self):
        """
        Return string representation

        :return:
        """
        if self.name:
            return f"{self.address} - {self.name}"
        return f"{self.address}"

    def __eq__(self, other):
        """
        Test equality on address

        :param other: Account instance
        :return:
        """
        if not isinstance(other, self.__class__):
            return False
        return other.address == self.address

    def __hash__(self):
        return hash(self.address)
