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
import json
import logging
from datetime import datetime, timedelta
from typing import List

from substrateinterface import Keypair

from tikka.domains.entities.technical_committee import (
    TechnicalCommitteeCall,
    TechnicalCommitteeProposal,
    TechnicalCommitteeVoting,
)
from tikka.interfaces.adapters.network.connection import NetworkConnectionError
from tikka.interfaces.adapters.network.technical_commitee import (
    NetworkTechnicalCommitteeException,
    NetworkTechnicalCommitteeInterface,
)


class NetworkTechnicalCommittee(NetworkTechnicalCommitteeInterface):
    """
    NetworkTechnicalCommittee class
    """

    def members(self) -> List[str]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTechnicalCommitteeInterface.members.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTechnicalCommitteeException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query("TechnicalCommittee", "Members")
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        if result.value is not None:
            return result.value
        return []

    def proposals(self) -> List[TechnicalCommitteeProposal]:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTechnicalCommitteeInterface.proposals.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTechnicalCommitteeException(NetworkConnectionError())

        try:
            result = self.connections.rpc.client.query(
                "TechnicalCommittee", "Proposals"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        proposal_hash_256_list = result.value

        try:
            current_block = self.connections.rpc.client.rpc_request(
                "system_syncState", []
            ).get("result")["currentBlock"]
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        try:
            result = self.connections.rpc.client.get_constant(
                "Babe", "ExpectedBlockTime"
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        block_duration_in_ms = result.value
        current_time = datetime.now()

        proposals = []
        for proposal_hash_256 in proposal_hash_256_list:

            # fetch Voting
            try:
                result = self.connections.rpc.client.query(
                    "TechnicalCommittee", "Voting", [proposal_hash_256]
                )
            except Exception as exception:
                logging.exception(exception)
                raise NetworkTechnicalCommitteeException(exception)

            block_diff = result.value["end"] - current_block
            if block_diff < 0:
                block_time = current_time - timedelta(
                    milliseconds=abs(block_diff) * block_duration_in_ms
                )
            else:
                block_time = current_time + timedelta(
                    milliseconds=abs(block_diff) * block_duration_in_ms
                )

            voting = TechnicalCommitteeVoting(
                result.value["index"],
                result.value["threshold"],
                result.value["ayes"],
                result.value["nays"],
                block_time,
            )

            # fetch Call
            try:
                result = self.connections.rpc.client.query(
                    "TechnicalCommittee", "ProposalOf", [proposal_hash_256]
                )
            except Exception as exception:
                logging.exception(exception)
                raise NetworkTechnicalCommitteeException(exception)

            call = TechnicalCommitteeCall(
                result.value["call_index"],
                result.value["call_hash"],
                result.value["call_module"],
                result.value["call_function"],
                json.dumps(result.value["call_args"]),
            )
            proposal = TechnicalCommitteeProposal(proposal_hash_256, call, voting)

            proposals.append(proposal)

        return proposals

    def vote(
        self, keypair: Keypair, proposal: TechnicalCommitteeProposal, vote: bool
    ) -> None:
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            NetworkTechnicalCommitteeInterface.proposals.__doc__
        )
        if not self.connections.is_connected() or self.connections.rpc.client is None:
            raise NetworkTechnicalCommitteeException(NetworkConnectionError())

        params = {
            "proposal": proposal.hash,
            "index": proposal.voting.index,
            "approve": vote,
        }

        try:
            call = self.connections.rpc.client.compose_call(
                call_module="TechnicalCommittee",
                call_function="vote",
                call_params=params,
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        try:
            extrinsic = self.connections.rpc.client.create_signed_extrinsic(
                call=call, keypair=keypair
            )
        except Exception as exception:
            logging.exception(exception)
            raise NetworkTechnicalCommitteeException(exception)

        # fixme: code stuck infinitely if no blocks are created on blockchain
        #       should have a timeout option
        result = self.connections.rpc.client.submit_extrinsic(
            extrinsic, wait_for_inclusion=True
        )
        logging.debug(
            "Extrinsic '%s' sent and included in block '%s'",
            result.extrinsic_hash,
            result.block_hash,
        )
        if result.is_success is False:
            logging.error(result.error_message)
            raise NetworkTechnicalCommitteeException(result.error_message["name"])
