import binascii
from typing import Union

from glitter_sdk.util.encrypt.converter.bech32 import bech32_decode
from glitter_sdk.util.encrypt.converter.bech32 import bech32_encode
from glitter_sdk.util.encrypt.converter.bech32 import convertbits
from glitter_sdk.util.encrypt.converter.bech32 import Encoding

EVMOS_PREFIX = 'glitter'
ETH_PREFIX = '0x'


def bech32_to_eth(wallet: str, prefix: str) -> Union[str, None]:
    decoded = bech32_decode(wallet)
    if decoded[0] != prefix:
        return None
    words = convertbits(decoded[1], 5, 8, False)
    res = ''
    for w in words:
        res = f'{res}{format(w, "x").zfill(2)}'

    return f'{ETH_PREFIX}{res}'


def eth_to_bech32(wallet: str, prefix: str) -> str:
    splitted = wallet.split('0x')
    if len(splitted) == 2:
        raw_address = splitted[1]
    else:
        raw_address = wallet
    try:
        array = binascii.unhexlify(raw_address)
        words = [x for x in array]
        bech32_words = convertbits(words, 8, 5)
        bech32_address = bech32_encode(prefix, bech32_words, Encoding.BECH32)
    except Exception:
        return None
    if len(bech32_address) != 46:
        return None

    return bech32_address


def glitter_to_eth(wallet: str) -> Union[str, None]:
    return bech32_to_eth(wallet, EVMOS_PREFIX)


def eth_to_glitter(wallet: str) -> str:
    return eth_to_bech32(wallet, EVMOS_PREFIX)
