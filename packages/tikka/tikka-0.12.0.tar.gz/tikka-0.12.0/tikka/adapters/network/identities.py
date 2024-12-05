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
import logging
import struct
from typing import List, Optional

from substrateinterface import Keypair
from substrateinterface.exceptions import SubstrateRequestException

from tikka.domains.entities.identity import Certification, Identity, IdentityStatus
from tikka.interfaces.adapters.network.connection import NetworkConnectionError
from tikka.interfaces.adapters.network.identities import (
    NetworkIdentitiesException,
    NetworkIdentitiesInterface,
)


class NetworkIdentities(NetworkIdentitiesInterface):
    """
    NetworkIdentities class
    """

    status_map = {
        "Unconfirmed": IdentityStatus.UNCONFIRMED,
        "Unvalidated": IdentityStatus.UNVALIDATED,
        "Member": IdentityStatus.MEMBER,
        "NotMember": IdentityStatus.NOT_MEMBER,
        "Revoked": IdentityStatus.REVOKED,
    }

    def get_identity_index(self, address: str) -> Optional[int]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity_index.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query(
                "Identity", "IdentityIndexOf", [address]
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        return result.value

    def get_identity_indice(self, addresses: List[str]) -> List[Optional[int]]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity_indice.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        storage_keys = []
        for address in addresses:
            storage_keys.append(
                self.connections.rpc.client.create_storage_key(
                    "Identity", "IdentityIndexOf", [address]
                )
            )

        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        identity_indice = []
        for index, (storage_key, value_obj) in enumerate(multi_result):
            identity_indice.append(value_obj.value)

        return identity_indice

    def get_identity(self, index: int) -> Optional[Identity]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identity.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query(
                "Identity", "Identities", [index]
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        if result is None:
            return None
        old_address = result["old_owner_key"].value
        if old_address is not None:
            old_address = old_address[0]
        return Identity(
            index=index,
            next_creatable_on=result["next_creatable_identity_on"].value,
            removable_on=int(result["next_scheduled"].value),
            status=self.status_map[result["status"].value],
            address=result["owner_key"].value,
            old_address=old_address,
        )

    def get_identities(self, identity_indice: List[int]) -> List[Optional[Identity]]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.get_identities.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        storage_keys = []
        for identity_index in identity_indice:
            storage_keys.append(
                self.connections.rpc.client.create_storage_key(
                    "Identity", "Identities", [identity_index]
                )
            )

        try:
            multi_result = self.connections.rpc.client.query_multi(storage_keys)
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        identities: List[Optional[Identity]] = []
        for index, (storage_key, value_obj) in enumerate(multi_result):
            if value_obj.value is not None:
                identities.append(
                    Identity(
                        index=storage_keys[index].params[0],
                        next_creatable_on=value_obj["next_creatable_identity_on"].value,
                        removable_on=int(value_obj["next_scheduled"].value),
                        status=self.status_map[value_obj["status"].value],
                        address=value_obj["owner_key"].value,
                        old_address=value_obj["old_owner_key"].value,
                    )
                )
            else:
                identities.append(None)

        return identities

    def change_owner_key(self, old_keypair: Keypair, new_keypair: Keypair) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.change_owner_key.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        identity_index = self.get_identity_index(old_keypair.ss58_address)
        if identity_index is None:
            raise NetworkIdentitiesException("No identity found for origin account")

        # message to sign
        prefix_bytes = b"icok"
        genesis_hash_str = self.connections.rpc.client.get_block_hash(0)
        genesis_hash_bytes = bytearray.fromhex(genesis_hash_str[2:])
        identity_index_bytes = struct.pack("<I", identity_index)
        identity_pubkey_bytes = old_keypair.public_key
        message_bytes = (
            prefix_bytes
            + genesis_hash_bytes
            + identity_index_bytes
            + identity_pubkey_bytes
        )

        # message signed by the new owner
        signature_bytes = new_keypair.sign(message_bytes)

        # newKey: AccountId32, newKeySig: SpRuntimeMultiSignature
        params = {
            "new_key": new_keypair.ss58_address,
            "new_key_sig": {"Sr25519": signature_bytes},
        }
        try:
            # create raw call (extrinsic)
            call = self.connections.rpc.client.compose_call(
                call_module="Identity",
                call_function="change_owner_key",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        try:
            # create extrinsic signed by current owner
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=old_keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        try:
            result = self.connections.rpc.client.submit_extrinsic(
                extrinsic, wait_for_inclusion=True
            )
        except SubstrateRequestException as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkIdentitiesException(result.error_message["name"])

    def certs_by_receiver(
        self, receiver_address: str, receiver_identity_index: int
    ) -> List[Certification]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkIdentitiesInterface.certs_by_receiver.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkIdentitiesException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query(
                "Certification", "CertsByReceiver", [receiver_identity_index]
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkIdentitiesException(exception)

        storage_keys = []
        for issuer_identity_index, cert_expire_on_block in result.value:
            storage_keys.append(
                self.connections.rpc.client.create_storage_key(
                    "Identity", "Identities", [issuer_identity_index]
                )
            )

        multi_result = self.connections.rpc.client.query_multi(storage_keys)

        certifications = []
        for index, (storage_key, value_obj) in enumerate(multi_result):
            certifications.append(
                Certification(
                    issuer_identity_index=storage_keys[index].params[0],
                    issuer_address=value_obj.value["owner_key"],
                    receiver_identity_index=receiver_identity_index,
                    receiver_address=receiver_address,
                    expire_on_block=result.value[index][1],
                )
            )

        return certifications
