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

from typing import List

from substrateinterface import Keypair

from tikka.domains.entities.technical_committee import TechnicalCommitteeProposal
from tikka.domains.events import EventDispatcher
from tikka.interfaces.adapters.network.technical_commitee import (
    NetworkTechnicalCommitteeInterface,
)


class TechnicalCommittee:
    """
    TechnicalCommittee domain class
    """

    def __init__(
        self,
        network: NetworkTechnicalCommitteeInterface,
        event_dispatcher: EventDispatcher,
    ):
        """
        Init TechnicalCommittee domain

        :param network: NetworkTechnicalCommitteeInterface instance
        :param event_dispatcher: EventDispatcher instance
        """

        self.network = network
        self.event_dispatcher = event_dispatcher

    def network_members(self) -> List[str]:
        """
        Return all members of Technical Committee from network

        :return:
        """
        return self.network.members()

    def network_proposals(self) -> List[TechnicalCommitteeProposal]:
        """
        Return all proposals with voting infos of Technical Committee from network

        :return:
        """
        return self.network.proposals()

    def network_vote(
        self, keypair: Keypair, proposal: TechnicalCommitteeProposal, vote: bool
    ) -> None:
        """
        Send Technical Committee Vote for proposal from Keypair

        :param keypair: Keypair instance
        :param proposal: TechnicalCommitteeProposal instance
        :param vote: True or False
        :return:
        """
        return self.network.vote(keypair, proposal, vote)
