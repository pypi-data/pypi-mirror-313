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

import abc

from tikka.interfaces.domains.connections import ConnectionsInterface


class NetworkCurrencyInterface(abc.ABC):
    """
    NetworkCurrencyInterface class
    """

    def __init__(self, connections: ConnectionsInterface) -> None:
        """
        Use connections to request currency informations

        :param connections: ConnectionsInterface instance
        :return:
        """
        self.connections = connections

    @abc.abstractmethod
    def get_token_decimals(self) -> int:
        """
        Return the number of decimals for the token storage
        ex: 2 = store centimes, 1 token = stored value / 100

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_token_symbol(self) -> str:
        """
        Return the token symbol of the currency

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_universal_dividend(self) -> int:
        """
        Return the universal dividend current amount

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_monetary_mass(self) -> int:
        """
        Return the monetary mass current amount

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_members_count(self) -> int:
        """
        Return the monetary mass current amount

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_expected_block_time(self) -> int:
        """
        Return the expected block time in ms

        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_epoch_duration(self) -> int:
        """
        Return the expected session time in ms

        :return:
        """
        raise NotImplementedError


class NetworkCurrencyException(Exception):
    """
    NetworkCurrencyException class
    """
