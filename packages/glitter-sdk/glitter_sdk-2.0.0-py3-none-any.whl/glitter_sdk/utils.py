# Copyright GlitterClient GmbH and GlitterClient contributors
# SPDX-License-Identifier: (Apache-2.0 AND CC-BY-4.0)
# Code is Apache-2.0 and docs are CC-BY-4.0

"""Set of utilities to support various functionalities of the driver.

Attributes:
    ops_map (dict): Mapping between operation strings and classes.
        E.g.: The string ``'CREATE'`` is mapped to
        :class:`~.CreateOperation`.
"""
from urllib.parse import urlparse, urlunparse

DEFAULT_NODE = 'http://sg1.testnet.glitter.link:26659'
DEFAULT_NODES = [
    'http://sg1.testnet.glitter.link:26659',
    'http://sg2.testnet.glitter.link:26659',
    'http://sg3.testnet.glitter.link:26659',
    'http://sg4.testnet.glitter.link:26659',
    'http://sg7.testnet.glitter.link:26659',
    'http://sg8.testnet.glitter.link:26659',
    'http://sg9.testnet.glitter.link:26659',
    'http://sg10.testnet.glitter.link:26659',
    'http://sg11.testnet.glitter.link:26659',
    'http://sg12.testnet.glitter.link:26659',
    'http://sg13.testnet.glitter.link:26659',
    'http://sg14.testnet.glitter.link:26659',
    'http://sg15.testnet.glitter.link:26659',
]


class CreateOperation:
    """Class representing the ``'CREATE'`` transaction operation."""


class TransferOperation:
    """Class representing the ``'TRANSFER'`` transaction operation."""


ops_map = {
    'CREATE': CreateOperation,
    'TRANSFER': TransferOperation,
}


def _normalize_operation(operation):
    """Normalizes the operation string. For now, this simply means
    converting the string to uppercase, looking it up in
    :attr:`~.ops_map`, and returning the corresponding class if
    present.

    Args:
        operation (str): The operation string to convert.

    Returns:
        The class corresponding to the string,
        :class:`~.CreateOperation` or :class:`~TransferOperation`.

        .. important:: If the :meth:`str.upper` step, or the
            :attr:`~.ops_map` lookup fails, the ``operation``
            argument is returned.

    """
    try:
        operation = operation.upper()
    except AttributeError:
        pass

    try:
        operation = ops_map[operation]()
    except KeyError:
        pass

    return operation


def _get_default_port(scheme):
    return 443 if scheme == 'https' else 9984


def normalize_url(node):
    """Normalizes the node url."""
    if not node:
        node = DEFAULT_NODE
    elif '://' not in node:
        node = '//{}'.format(node)
    parts = urlparse(node, scheme='http', allow_fragments=False)
    port = parts.port if parts.port else _get_default_port(parts.scheme)
    netloc = '{}:{}'.format(parts.hostname, port)
    return urlunparse((parts.scheme, netloc, parts.path, '', '', ''))


def normalize_node(node, headers=None):
    """Normalizes the node as str or dict with headers."""
    headers = {} if headers is None else headers
    if isinstance(node, str):
        url = normalize_url(node)
        return {'endpoint': url, 'headers': headers}

    url = normalize_url(node['endpoint'])
    node_headers = node.get('headers', {})
    return {'endpoint': url, 'headers': {**headers, **node_headers}}


def normalize_nodes(*nodes, headers=None):
    """Normalizes the dict or array of driver nodes."""
    if not nodes:
        nodes = DEFAULT_NODES

    normalized_nodes = ()
    for node in nodes:
        normalized_nodes += (normalize_node(node, headers),)
    return normalized_nodes
