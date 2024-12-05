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
from typing import List, Optional

from substrateinterface import Keypair

from tikka.domains.entities.identity import Certification, Identity, IdentityStatus
from tikka.interfaces.adapters.network.identities import NetworkIdentitiesInterface
from tikka.interfaces.adapters.repository.identities import (
    IdentitiesRepositoryInterface,
)


class Identities:

    """
    Identities domain class
    """

    def __init__(
        self,
        repository: IdentitiesRepositoryInterface,
        network: NetworkIdentitiesInterface,
    ):
        """
        Init Accounts domain

        :param repository: AccountsRepositoryInterface instance
        :param network: NetworkAccountsInterface instance
        """
        self.repository = repository
        self.network = network

    @staticmethod
    def create(
        index: int,
        removable_on: int,
        next_creatable_on: int,
        address: str,
        old_address: Optional[str],
        status: IdentityStatus = IdentityStatus.UNCONFIRMED,
    ):
        """
        Return an identity instance from params

        :param index: Index number in blockchain
        :param removable_on: Identity expiration timestamp
        :param next_creatable_on: Date after which a new identity can be created
        :param address: Account address
        :param old_address: Previous account address
        :param status: Identity status
        :return:
        """
        return Identity(
            index=index,
            removable_on=removable_on,
            next_creatable_on=next_creatable_on,
            status=status,
            address=address,
            old_address=old_address,
        )

    def add(self, identity: Identity):
        """
        Add identity in repository

        :param identity: Identity instance
        :return:
        """
        self.repository.add(identity)

    def update(self, identity: Identity):
        """
        Update identity in repository

        :param identity: Identity instance
        :return:
        """
        self.repository.update(identity)

    def get(self, index: int) -> Optional[Identity]:
        """
        Get identity instance

        :param index: Identity index
        :return:
        """
        return self.repository.get(index)

    def get_by_address(self, address: str) -> Optional[Identity]:
        """
        Return Identity instance from account address or None

        :param address: Account address
        :return:
        """
        return self.repository.get_by_address(address)

    def get_index_by_address(self, address: str) -> Optional[int]:
        """
        Return identity index from account address or None

        :param address: Account address
        :return:
        """
        return self.repository.get_index_by_address(address)

    def delete(self, index: int) -> None:
        """
        Delete identity in repository

        :param index: Identity index to delete
        :return:
        """
        self.repository.delete(index)

    def exists(self, index: int) -> bool:
        """
        Return True if identity exists in repository

        :param index: Identity index to check
        :return:
        """
        return self.repository.exists(index)

    def is_validated(self, index: int) -> bool:
        """
        Return True if identity status is validated

        :param index: Identity index to check
        :return:
        """
        identity = self.get(index)
        if identity is None:
            return False
        return identity.status == IdentityStatus.MEMBER

    def network_get_index(self, address: str) -> Optional[int]:
        """
        Get account identity index from network if any

        :param address: Account address
        :return:
        """
        identity_index = self.network.get_identity_index(address)
        if identity_index is None:
            old_identity_index = self.get_index_by_address(address)
            if old_identity_index is not None:
                self.delete(old_identity_index)

        return identity_index

    def network_get_identity_indice(self, addresses: List[str]) -> List[Optional[int]]:
        """
        Get account identity indice from current EntryPoint connection

        :param addresses: List of Account addresses
        :return:
        """
        identity_indice = self.network.get_identity_indice(addresses)
        # todo: purge smiths db from if index
        # todo: purge authorities db if None index
        for index, address in enumerate(addresses):
            if identity_indice[index] is None:
                identity_index = self.get_index_by_address(address)
                if identity_index is not None:
                    self.delete(identity_index)

        return identity_indice

    def network_get_identity(self, index: int) -> Optional[Identity]:
        """
        Get Identity instance by index from network if any

        :param index: Identity index
        :return:
        """
        identity = self.network.get_identity(index)
        if identity is not None:
            if self.exists(index) is True:
                self.update(identity)
            else:
                self.add(identity)

        return identity

    def network_get_identities(self, identity_indice: List[int]) -> None:
        """
        Get Identity instances by index list from network

        :param identity_indice: Identity index list
        :return:
        """
        identities = self.network.get_identities(identity_indice)
        for index, identity in enumerate(identities):
            if identity is None:
                self.repository.delete(identity_indice[index])
                continue
            if self.exists(identity.index) is True:
                self.update(identity)
            else:
                self.add(identity)

    def network_change_owner_key(
        self, old_keypair: Keypair, new_keypair: Keypair
    ) -> None:
        """
        Change identity owner from old_keypair to new_keypair on blockchain

        :param old_keypair: Keypair of current identity account
        :param new_keypair: Keypair of new identity account
        :return:
        """
        return self.network.change_owner_key(old_keypair, new_keypair)

    def network_get_certs_by_receiver(
        self, receiver_address: str, receiver_identity_index: int
    ) -> Optional[List[Certification]]:
        """
        Get certification (identity index, expire on block number) list for identity index from network if any

        :param receiver_address: Address of receiver account
        :param receiver_identity_index: Identity index of receiver
        :return:
        """
        return self.network.certs_by_receiver(receiver_address, receiver_identity_index)
