from __future__ import annotations

import json
import requests
from betterproto import Casing
from typing import Optional, Tuple, Any
from glitter_sdk.core.tx import SignMode, Tx
from glitter_sdk.key.key import Key, SignOptions
from glitter_sdk.core.bank import MsgMultiSend, MsgSend
from glitter_sdk.client.lcd.api.tx import CreateTxOptions, SignerOptions
from glitter_sdk.core.msgs import CreateDatasetRequest, EditDatasetRequest, RenewalDatasetRequest, EditTableRequest, \
    PledgeRequest, ReleasePledgeRequest
from glitter_proto.glitterchain.index import ServiceStatus, TableDesc, DatasetDesc

from grpclib.client import Channel
from glitter_proto.glitterchain.index import QueryStub as IndexQueryStub, QueryDatesetRequest, \
    QueryDatesetResponse, QueryDatesetsRequest, QueryDatesetsResponse
from glitter_proto.glitterchain.consumer import QueryStub as ConsumerQueryStub

__all__ = ["DataSet", ]


class QueryArgument:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class DataSet():
    """Wraps around a :class:`Key` implementation and provides transaction building and
    signing functionality. It is recommended to create this object through
    :meth:`LCDClient.DB()<glitter_sdk.client.lcd.LCDClient.DB>`."""

    def __init__(self, lcd, key: Key):
        self.lcd = lcd
        self.key = key

    def account_number(self) -> int:
        """
        Fetches account number for the account associated with the Key.

        Returns:
          Account number as integer
        """
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.account_number

    def sequence(self) -> int:
        """
        Fetches the sequence number for the account associated with the Key.

        Returns:
          Account sequence number as integer
        """
        res = self.lcd.auth.account_info(self.key.acc_address)
        return res.sequence

    def account_number_and_sequence(self) -> dict:
        """
        Fetches both account and sequence number associated with the Key

        Returns:
          Account number and sequence as a dict
        """
        res = self.lcd.auth.account_info(self.key.acc_address)
        return {"account_number": res.get_account_number(), "sequence": res.get_sequence()}

    def create_tx(self, options: CreateTxOptions) -> Tx:
        """ Builds an unsigned transaction object. The ``DB`` will first
        query the blockchain to fetch the latest ``account`` and ``sequence`` values for the
        account corresponding to its Key, unless the they are both provided. If no ``fee``
        parameter is set, automatic fee estimation will be used (see `fee_estimation`).

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: unsigned transaction
        """
        sigOpt = [
            SignerOptions(
                address=self.key.acc_address,
                sequence=options.sequence,
                public_key=self.key.public_key,
            )
        ]
        return self.lcd.tx.create(sigOpt, options)

    def create_and_sign_tx(self, options: CreateTxOptions) -> Tx:
        """Creates and signs a :class:`Tx` object in a single step. This is the recommended
        method for preparing transaction for immediate signing and broadcastring. The transaction
        is generated exactly as :meth:`create_tx`.

        Args:
            options (CreateTxOptions): Options to create a tx

        Returns:
            Tx: signed transaction
        """

        account_number = options.account_number
        sequence = options.sequence
        if account_number is None or sequence is None:
            res = self.account_number_and_sequence()
            if account_number is None:
                account_number = res.get("account_number")
            if sequence is None:
                sequence = res.get("sequence")
        options.sequence = sequence
        options.account_number = account_number
        return self.key.sign_tx(
            tx=self.create_tx(options),
            options=SignOptions(
                account_number=account_number,
                sequence=sequence,
                chain_id=self.lcd.chain_id,
                sign_mode=options.sign_mode
                if options.sign_mode
                else SignMode.DIRECT,
            ),
        )

    def create_dataset(self, dataset_name: str, host: str, description: DatasetDesc,
                       work_status: ServiceStatus = ServiceStatus.Service_Status_Start,
                       duration: int = 86400 * 365):
        """
        Create a new dataset with the specified name.

        Args:
          dataset_name: The name of the dataset to create
          host: The hostname or IP address of the dataset server,usually engine-server address.
          description: A brief description of the dataset being created (e.g.,{}).
          work_status: The current status of the service (e.g., START, STOP, DELETE).
          duration: The duration (in seconds) for which the dataset should be maintained.

        Returns:
          The result of executing the  CREATE DataSet transaction
        """
        # to_dict converts integer field values to strings
        desc = description.to_dict(casing=Casing.SNAKE, include_default_values=True)
        desc["row_cnt"] = description.row_cnt

        msg = CreateDatasetRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            work_status=work_status,
            hosts=host,
            manage_addresses="",
            description=json.dumps(desc),
            duration=duration,
        )
        option = CreateTxOptions(
            msgs=[msg],
            memo="create dataset transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )
        tx = self.create_and_sign_tx(option)
        return self.lcd.tx.broadcast(tx)

    def edit_dataset(self, dataset_name: str, host: str, description: DatasetDesc,
                     work_status: ServiceStatus = ServiceStatus.Service_Status_Start):
        """
        Edit an existing dataset with the specified parameters.

        Args:
          from_address: sign address of the dataset
          dataset_name: The name of the dataset to create
          host: The hostname or IP address of the dataset server,usually engine-server address.
          description: A brief description of the dataset being created (e.g.,{}).
          work_status: The current status of the service (e.g., START, STOP, DELETE).
                Defaults to ServiceStatus.Service_Status_Start.

        Returns:
            None: This method does not return a value. It modifies the dataset in place.

        Raises:
            ValueError: If the dataset_name is empty or if the host is invalid.
            Exception: For any other errors encountered during the editing process.
        """

        # to_dict converts integer field values to strings
        desc = description.to_dict(casing=Casing.SNAKE, include_default_values=True)
        desc["row_cnt"] = description.row_cnt

        msg = EditDatasetRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            hosts=host,
            description=json.dumps(desc),
            work_status=work_status,
            manage_addresses="",
        )
        option = CreateTxOptions(
            msgs=[msg],
            memo="edit dataset transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )
        tx = self.create_and_sign_tx(option)
        return self.lcd.tx.broadcast(tx)

    def renewal_dataset(self, dataset_name: str, duration: int = 86400 * 365):
        msg = RenewalDatasetRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            duration=duration,
        )
        option = CreateTxOptions(
            msgs=[msg],
            memo="renewal dataset transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )
        tx = self.create_and_sign_tx(option)
        return self.lcd.tx.broadcast(tx)

    def edit_table(self, dataset_name: str, table: str, description: TableDesc):
        """
        Edit a table in a specified dataset.

        Args:
            dataset_name (str): The name of the dataset containing the table.
            table (str): The name of the table to edit.
            description (str): A brief description of the changes made.

        Returns:
            A tuple containing the transaction response and any error encountered.
        """
        msg = EditTableRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            table_name=table,
            description=description.to_json(),
        )
        option = CreateTxOptions(
            msgs=[msg],
            memo="edit table transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )
        tx = self.create_and_sign_tx(option)
        return self.lcd.tx.broadcast(tx)

    def pledge(self, dataset_name: str, amount: str):
        """
        Pledge an amount to a specified dataset.

        Args:
            dataset_name (str): The name of the dataset to pledge to.
            amount (str): The amount to pledge.

        Returns:
             A tuple containing the transaction response and any error encountered.
        """
        msg = PledgeRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            amount=amount,
        )

        options = CreateTxOptions(
            msgs=[msg],
            memo="pledge transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )

        tx = self.create_and_sign_tx(options)
        return self.lcd.tx.broadcast(tx)

    def release_pledge(self, dataset_name: str, amount: str):
        msg = ReleasePledgeRequest(
            from_address=self.key.acc_address,
            dataset_name=dataset_name,
            amount=amount,
        )

        options = CreateTxOptions(
            msgs=[msg],
            memo="release pledge transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        )

        tx = self.create_and_sign_tx(options)
        return self.lcd.tx.broadcast(tx)

    def query(self, dataset_name: str, sql: str, arguments: list[QueryArgument] = None) -> Tuple[Any, str]:
        """
        Execute a SQL query statement against a specified dataset.

        Args:
            dataset_name (str): The name of the dataset to query.
            sql (str): The SQL query string to be executed.
            arguments (Optional[List[QueryArgument]]): 
                An optional list of QueryArgument objects to substitute into the query.
                Each argument should be an instance of QueryArgument with the necessary attributes.

        Returns:
            Tuple[Optional[str], Optional[str]]:
                A tuple containing:
                - A string representing the response text from the query execution (or an empty string in case of an error).
                - An optional string containing an error message (or None if the query was successful).

        Raises:
            requests.RequestException: If there is an issue with the HTTP request.
        """
        host, err = self.get_dataset_host(dataset_name)
        if err is not None or host == "":
            return "", err

        engine_host = f"{host}/api/v1/simple_sql_query"
        engine_param = {"sql": sql, "arguments": [arg.__dict__ for arg in arguments]}

        try:
            response = requests.post(engine_host, json=engine_param)
            response.raise_for_status()
            return response.json(), ""
        except requests.RequestException as e:
            return "", str(e)

    def get_dataset_host(self, dataset_name: str) -> Tuple[str, str]:
        """
        Retrieve the host information for a specified dataset.

        Args:
            dataset_name (str): The name of the dataset for which to retrieve the host information.

        Returns:
            Tuple[str, str]:
                A tuple containing:
                - A string representing the host(s) associated with the dataset (or an empty string in case of an error).
                - An string containing an error message (or an empty string if the operation was successful).
        """
        path = "/glitterchain/index/dataset/"
        url = f"{self.url}{path}{dataset_name}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['hosts'], ""
        except requests.RequestException as e:
            return "", str(e)

    def transfer(self, addr: str, amount: str):
        """
        Transfer tokens to address

        Args:
          addr: Recipient address
          amount: Amount to transfer

        Returns:
          Result of broadcasting transaction
        """

        tx = self.create_and_sign_tx(CreateTxOptions(
            msgs=[MsgSend(
                self.key.acc_address,
                addr,
                amount
            )],
            memo="bank send transaction!",
            fee_denoms=["agli"],
            sign_mode=SignMode.DIRECT,
            gas="auto",
        ))
        return self.lcd.tx.broadcast(tx)

    async def query_cpdts(
            self,
            query_cpd_ts_request: "QueryCpdTsRequest",
            *,
            timeout: Optional[float] = None,
            deadline: Optional["Deadline"] = None,
            metadata: Optional["MetadataLike"] = None
    ) -> "QueryCpdTsResponse":
        return super().query_cpdts(query_cpd_ts_request, timeout=timeout, deadline=deadline, metadata=metadata)
