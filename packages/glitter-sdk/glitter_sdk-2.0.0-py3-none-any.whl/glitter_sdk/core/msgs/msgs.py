"""Bank module message types."""

from __future__ import annotations

from glitter_proto.glitterchain.index import CreateDatasetRequest as CreateDatasetRequest_pb, ServiceStatus
from glitter_proto.glitterchain.index import EditDatasetRequest as EditDatasetRequest_pb
from glitter_proto.glitterchain.index import RenewalDatasetRequest as RenewalDatasetRequest_pb
from glitter_proto.glitterchain.index import EditTableRequest as EditTableRequest_pb
from glitter_proto.glitterchain.consumer import PledgeRequest as PledgeRequest_pb
from glitter_proto.glitterchain.consumer import ReleasePledgeRequest as ReleasePledgeRequest_pb

from glitter_sdk.core.msg import Msg

__all__ = ["CreateDatasetRequest", "EditDatasetRequest", "RenewalDatasetRequest", "EditTableRequest", "PledgeRequest",
           "ReleasePledgeRequest"]

import attr


@attr.s
class CreateDatasetRequest(Msg):
    type_amino = "cosmos-sdk/CreateDatasetRequest"
    """"""
    type_url = "/glitterchain.index.CreateDatasetRequest"
    """"""
    action = "send"
    """"""
    prototype = CreateDatasetRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    work_status: ServiceStatus = attr.ib()
    hosts: str = attr.ib()
    manage_addresses: str = attr.ib()
    description: str = attr.ib()
    duration: int = attr.ib()

    @classmethod
    def from_proto(cls, proto: CreateDatasetRequest_pb) -> CreateDatasetRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            work_status=proto.work_status,
            hosts=proto.hosts,
            manage_addresses=proto.manage_addresses,
            description=proto.description,
            duration=proto.duration,
        )

    def to_proto(self) -> CreateDatasetRequest_pb:
        proto = CreateDatasetRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.work_status = self.work_status
        proto.hosts = self.hosts
        proto.manage_addresses = self.manage_addresses
        proto.description = self.description
        proto.duration = self.duration
        return proto


@attr.s
class EditDatasetRequest(Msg):
    type_amino = "cosmos-sdk/EditDatasetRequest"
    """"""
    type_url = "/glitterchain.index.EditDatasetRequest"
    """"""
    action = "send"
    """"""
    prototype = EditDatasetRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    work_status: ServiceStatus = attr.ib()
    hosts: str = attr.ib()
    manage_addresses: str = attr.ib()
    description: str = attr.ib()

    @classmethod
    def from_proto(cls, proto: EditDatasetRequest_pb) -> EditDatasetRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            work_status=proto.work_status,
            hosts=proto.hosts,
            manage_addresses=proto.manage_addresses,
            description=proto.description,
        )

    def to_proto(self) -> EditDatasetRequest_pb:
        proto = EditDatasetRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.work_status = self.work_status
        proto.hosts = self.hosts
        proto.manage_addresses = self.manage_addresses
        proto.description = self.description
        return proto


@attr.s
class RenewalDatasetRequest(Msg):
    type_amino = "cosmos-sdk/RenewalDatasetRequest"
    """"""
    type_url = "/glitterchain.index.RenewalDatasetRequest"
    """"""
    action = "send"
    """"""
    prototype = RenewalDatasetRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    duration: int = attr.ib()

    @classmethod
    def from_proto(cls, proto: RenewalDatasetRequest_pb) -> RenewalDatasetRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            duration=proto.duration,
        )

    def to_proto(self) -> RenewalDatasetRequest_pb:
        proto = RenewalDatasetRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.duration = self.duration
        return proto


@attr.s
class EditTableRequest(Msg):
    type_amino = "cosmos-sdk/EditTableRequest"
    """"""
    type_url = "/glitterchain.index.EditTableRequest"
    """"""
    action = "send"
    """"""
    prototype = EditTableRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    table_name: str = attr.ib()
    description: str = attr.ib()

    @classmethod
    def from_proto(cls, proto: EditTableRequest_pb) -> EditTableRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            table_name=proto.table_name,
            description=proto.description,
        )

    def to_proto(self) -> EditTableRequest_pb:
        proto = EditTableRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.table_name = self.table_name
        proto.description = self.description
        return proto


@attr.s
class PledgeRequest(Msg):
    type_amino = "cosmos-sdk/PledgeRequest"
    """"""
    type_url = "/glitterchain.consumer.PledgeRequest"
    """"""
    action = "send"
    """"""
    prototype = PledgeRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    amount: str = attr.ib()

    @classmethod
    def from_proto(cls, proto: PledgeRequest_pb) -> PledgeRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            amount=proto.amount,
        )

    def to_proto(self) -> PledgeRequest_pb:
        proto = PledgeRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.amount = self.amount
        return proto


@attr.s
class ReleasePledgeRequest(Msg):
    type_amino = "cosmos-sdk/ReleasePledgeRequest"
    """"""
    type_url = "/glitterchain.consumer.ReleasePledgeRequest"
    """"""
    action = "send"
    """"""
    prototype = ReleasePledgeRequest_pb
    """"""
    from_address: str = attr.ib()
    dataset_name: str = attr.ib()
    amount: str = attr.ib()

    @classmethod
    def from_proto(cls, proto: ReleasePledgeRequest_pb) -> ReleasePledgeRequest:
        return cls(
            from_address=proto.from_address,
            dataset_name=proto.dataset_name,
            amount=proto.amount,
        )

    def to_proto(self) -> ReleasePledgeRequest_pb:
        proto = ReleasePledgeRequest_pb()
        proto.from_address = self.from_address
        proto.dataset_name = self.dataset_name
        proto.amount = self.amount
        return proto
