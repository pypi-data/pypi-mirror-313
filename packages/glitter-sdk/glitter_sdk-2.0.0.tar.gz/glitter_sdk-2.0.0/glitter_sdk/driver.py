# Copyright GlitterClient GmbH and GlitterClient contributors
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

from .transport import Transport
from .utils import normalize_nodes

class GlitterClient:
    """A :class: `~driver.GlitterClient` is a python client for Glitter. We can
      use this client to connect, create schema and put & search documents in
      Glitter.

    """

    def __init__(self, *nodes, headers=None, transport_class=Transport,
                 timeout=10):
        """Initializes a :class:`~driver.GlitterClient` driver instance.

        Args:
            *nodes (list of (str or dict)): Glitter nodes to connect to.
            headers (dict): Optional headers that will be passed with
             each request.
            transport_class: Optional transport class to use.
            timeout (int): Optional timeout in seconds that will be passed to
             each request.
        """
        self._headers = headers
        self._nodes = normalize_nodes(*nodes, headers=headers)
        self._transport = transport_class(*self._nodes, timeout=timeout)
        self._db = DataBase(self)
        self._chain = Chain(self)
        self._admin = Admin(self)
        self.api_prefix = '/v1'

    @property
    def nodes(self):
        """:obj:`tuple` of :obj:`str`:
         URLs of connected nodes.
        """
        return self._nodes

    @property
    def transport(self):
        """:class:`~driver.Transport`: Object responsible for forwarding
        requests to a :class:`~driver.Connection` instance (node).
        """
        return self._transport

    @property
    def chain(self):
        """:class:`~driver.Chain`: Used to query block or transaction info.
        """
        return self._chain

    @property
    def admin(self):
        """:class:`~driver.Admin`: Exposes functionalities of the ``'/admin'``
        endpoint.
        """
        return self._admin

    @property
    def db(self):
        """:class:`~driver.DataBase`: put or search doc from Glitter.
        """
        return self._db


class NamespacedDriver:
    """Base class for creating endpoints (namespaced objects) that can be added
     under the :class:`~driver.GlitterClient` driver.
    """

    PATH = '/'

    def __init__(self, driver):
        """Initializes an instance of
        :class:`~GlitterClient_driver.driver.NamespacedDriver` with the given
        driver instance.

        Args:
            driver (GlitterClient): Instance of
             :class:`~GlitterClient_driver.driver.GlitterClient`.
        """
        self.driver = driver

    @property
    def transport(self):
        return self.driver.transport

    @property
    def api_prefix(self):
        return self.driver.api_prefix

    @property
    def path(self):
        return self.api_prefix + self.PATH


class DataBase(NamespacedDriver):
    """DB to get access of the data in Glitter.
    """

    def create_schema(self, schema_name, fields):
        """

        Args:
            - schema_name (str): name of the schema.
            - fields (:obj:`list` of :obj:`dic`): list of schema fields in
             JSON format. It's required to specify the type field under the
             index field. O.w., get_doc functions are not able to be used.
             For more details, please follow instructions at
             https://docs.glitterprotocol.io.

        Returns:
            - :obj:`dic`: request result.
        """
        path = '/create_schema'
        schema_type = "record"
        body = {
            "schema_name": schema_name,
            "data": {
                "type": schema_type,
                "name": schema_name,
                "fields": fields
            }
        }

        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json=body,
        )

    def list_schema(self):
        """

        Returns:
            - :obj:`dic`: list all the schemas.
        """
        path = '/list_schema'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def get_schema(self, schema_name):
        """

        Args:
            - schema_name (str): name of the schema.
        Returns:
            - :obj:`dic`: detailed information of the schema.
        """
        path = '/get_schema'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"schema_name": schema_name}
        )

    def app_status(self):
        """

        Returns:
            - :obj:`dic`: a list of data schemas in Glitter along with the
             record counts.
        """

        path = '/app_status'

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def put_doc(self, schema_name, doc_data):
        """Put document to Glitter.

        Args:
            - schema_name (str): name of the schema.
            - doc_data (:obj:`dic`): doc content.

        Returns:
            - :obj:`dic`: put doc transaction result with code, msg, tx.
        """
        path = '/put_doc'
        body = {
            "schema_name": schema_name,
            "doc_data": doc_data,
        }
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json=body,
        )

    def get_doc(self, schema_name, primary_key):
        """Get documents from Glitter by the primary key.

        Args:
            schema_name (str): name of the schema.
            primary_key: a unique key of the document.

        Returns:
            :obj:`dic`: result with the document struct.
        """
        path = '/get_docs'
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json={"schema_name": schema_name, "doc_ids": [primary_key]},
        )

    def get_docs(self, schema_name, primary_key):
        """Get documents from glitter by doc ids.

        Args:
            schema_name (str): name of the schema.
            primary_key (list): keys of the documents and each of them must be
             unique.

        Returns:
            :obj:`dic`: detailed documents in Glitter.
        """
        path = '/get_docs'
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json={"schema_name": schema_name, "doc_ids": primary_key},
        )

    def search(self, schema_name, query_word, query_field=[], filters=[],
               aggs_field=[], order_by="", limit=10, page=1):
        """Search from Glitter specified by the conditions and filters.

        Args:
            schema_name (str): name of the schema.
            query_word (str): word to search in the query_field.
            query_field (:obj: `list` of str): a list of the fields to search.
             If it's empty, will search all the fields.
            filters (:obj:`list` of :obj:`dic`): filter conditions.
            aggs_field (:obj: `list` of str): aggregated field which is defined
             in the schema. Aggregation a multi-bucket value source based
             aggregation, where buckets are dynamically built - one per unique
             value.
            order_by (str): adds a sort order.
            limit(int): sets an upper limit on the response body size that we
             accept.
            page(int): page index to start the search from.

        Returns:
            :obj:`dic`: a list of documents which have matched query word in
            their fields.
        """

        path = '/search'
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            json={"index": schema_name, "query": query_word, "filters": filters,
                  "query_field": query_field, "aggs_field": aggs_field,
                  "order_by": order_by, "limit": limit, "page": page},
        )


class Chain(NamespacedDriver):
    PATH = '/chain/'

    def status(self):
        """ Get Tendermint status including node info, pubkey, latest block
         hash, app hash, block height, current max peer height and time.

        Returns:
            :obj:`json`: Details of the HTTP API provided by the
            Tendermint server.
        """
        path = "/chain/status"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def tx_search(self, query, page=1, per_page=30, order_by="desc",
                  prove=True):
        """Search for transactions.

        Args:
            query (str): query words. (e.g: ``tx.height=1000, tx.hash='xxx',
             update_doc.token='test_token'``)
            page (int): page index to start the search from. Defaults to ``1``.
            per_page (int): number of entries per page
             (max: ``100``,defaults to ``30``) .
            order_by (str): Sort the returned transactions (``asc`` or ``desc``) 
             by height & index . If it's empty, desc is used as default.
            prove (bool): Include proofs of the transactions in the
             block. Defaults to ``True``. (This is an option to the tendermint
             concept, indicating whether the return value is included in the
             block's transaction proof.)

        Returns:
            :obj"`json`: transaction info.
        """

        path = "/chain/tx_search"
        query = '"{}"'.format(query)
        order_by = '"{}"'.format(order_by)
        prove = "true" if prove else "false"

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={'query': query, 'page': page, 'per_page': per_page,
                    'order_by': order_by, 'prove': prove},
        )

    def block_search(self, query, page=1, per_page=30, order_by="desc"):
        """Search for blocks by BeginBlock and EndBlock events (BeginBlock and
         EndBlock is the concept of tendermint.
          https://docs.tendermint.com/master/spec/abci/apps.html#beginblock)

        Args:
            query (str): query condition. (e.g: ``block.height > 1000 AND
             valset.changed > 0``)
            page (int): page index to start the search from.
            per_page (int): number of entries per page (max: 100)
            order_by (str): sort the returned blocks ("asc" or "desc") by
             height. If it's empty, desc is used as default.
        Returns:
            :obj:`json`: block info.

        """
        path = "/chain/block_search"
        query = '"{}"'.format(query)
        order_by = '"{}"'.format(order_by)

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={'query': query, 'page': page,
                    'per_page': per_page, 'order_by': order_by},
        )

    def block(self, height=None):
        """ Get block at a specific height.

        Args:
            height (int): height

        Returns:
            :obj:`json`: a block with the specific height to return. If no
             height is provided, it will fetch the latest block.

        """
        path = "/chain/block"
        params = {}
        if height is not None:
            params["height"] = height
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params=params,
        )

    def health(self):
        """ Get health of the node.

        Returns:
            Details of the HTTP API provided by the Tendermint server, empty
             result (200 OK) on success, no response - in case of an error.
        """
        path = "/chain/health"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def net_info(self):
        """ Get network info.

        Returns:
            Details of the HTTP API provided by the tendermint server.

        """
        path = "/chain/net_info"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
        )

    def blockchain(self, min_height=1, max_height=20):
        """ Get block headers from max(minHeight, earliest available height) to
         min(maxHeight, current height) (inclusive).
         At most 20 items will be returned. Block headers are returned in
          descending order(highest first).

        Args:
            min_height (int): minimum block height to return.
            max_height (bool): maximum block height to return.

        Returns:
            Block headers returned in descending order (highest first).
        """

        path = "/chain/blockchain"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"minHeight": min_height, "maxHeight": max_height}
        )

    def header(self, height=1):
        """ Retrieve the block header corresponding to a specific height.

        Args:
            height (int): Fetch header with the height. If height is not set,
             return the lastest header.

        Returns:
            Header information.

        """
        path = "/chain/header"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"height": height},
        )

    def header_by_hash(self, header_hash):
        """ Retrieve the block header corresponding to a block hash.

        Args:
            header_hash (str): hash of the block.
        Returns:
        """
        path = "/chain/header_by_hash"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"hash": header_hash},
        )

    def block_by_hash(self, *, header_hash):
        """ Get block by hash.

        Args:
            header_hash (str): hash of the block, for example:
            "0xD70952032620CC4E2737EB8AC379806359D8E0B17B0488F627997A0B043ABDED"

        Returns:

        """
        path = "/chain/header_by_hash"
        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params={"hash": header_hash},
        )


class Admin(NamespacedDriver):
    """``'/admin'`` endpoint whi is used to manage the nodes.
    """

    def update_validator(self, pub_key, power=0, headers=None):
        """Update validator set. A validator is a peer who can vote.

        Args:
            pub_key (str): public key
            power (int): power
            headers (dict): http header

        Returns:
            :obj:`dic`: validator information.

        """
        path = "/admin/update_validator"
        return self.transport.forward_request(
            method='POST',
            path=self.api_prefix + path,
            params={'pub_key': pub_key, 'power': power},
            headers=headers
        )

    def validators(self, height=None, page=1, per_page=100):
        """ Get validator set at a specific height.

        Args:
            height (str): Fetch validators with the specific height. If height 
             is not set, return the lastest validator.
            page (int): page index to start the search from. (1-based)
            per_page (int): Number of entries per page (max: 100)

        Returns:
            :obj:`json`: A list of Validators which are sorted first by voting
             power (descending), then by address (ascending).

        """
        path = "/chain/validators"
        params = {"page": page, "per_page": per_page}
        if height is not None:
            params["height"] = height

        return self.transport.forward_request(
            method='GET',
            path=self.api_prefix + path,
            params=params,
        )
