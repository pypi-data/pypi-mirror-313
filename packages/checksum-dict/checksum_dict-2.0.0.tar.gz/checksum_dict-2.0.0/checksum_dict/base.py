from typing import TYPE_CHECKING, Dict, Iterable, Tuple, TypeVar, Union

from checksum_dict import exceptions
from checksum_dict._key import EthAddressKey

if TYPE_CHECKING:
    from checksum_dict._key import AnyAddressOrContract
else:
    from eth_typing import AnyAddress as AnyAddressOrContract


T = TypeVar("T")

_SeedT = Union[Dict[AnyAddressOrContract, T], Iterable[Tuple[AnyAddressOrContract, T]]]


class ChecksumAddressDict(Dict[EthAddressKey, T]):
    """
    A dictionary that maps Ethereum addresses to objects, automatically checksumming
    the provided address key when setting and getting values.

    If a `seed` dictionary or iterable of key-value pairs is provided, the keys will
    be added and the values will be set accordingly. The keys are checksummed when
    they are set using the `__setitem__` method. If `seed` is not provided or is `None`,
    the dictionary is initialized without any entries.

    Note:
        This implementation uses a :mod:`cchecksum`'s Cython implementation for checksumming to optimize
        performance over the standard :func:`eth_utils.to_checksum_address`.

    Examples:
        Creating a ChecksumAddressDict with a seed dictionary:

        >>> from checksum_dict import ChecksumAddressDict
        >>> seed = {"0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb": True}
        >>> d = ChecksumAddressDict(seed)
        >>> print(d)
        ChecksumAddressDict({'0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB': True})

        Creating an empty ChecksumAddressDict:

        >>> d = ChecksumAddressDict()
        >>> print(d)
        ChecksumAddressDict({})

        Accessing and setting items:

        >>> lower = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"
        >>> d[lower] = False
        >>> print(d[lower])
        False

    See Also:
        - :class:`EthAddressKey` for details on how keys are checksummed.
    """

    def __init__(self, seed: _SeedT = None) -> None:
        self.__dict__ = self
        if isinstance(seed, dict):
            seed = seed.items()
        if isinstance(seed, Iterable):
            for key, value in seed:
                self[key] = value

    def __repr__(self) -> str:
        return f"ChecksumAddressDict({str(dict(self))})"

    def __getitem__(self, key: AnyAddressOrContract) -> T:
        try:
            # It is ~700x faster to perform this check and then skip the checksum if we find a result for this key
            return dict.__getitem__(self, key)
        except KeyError:
            # NOTE: passing instead of checksumming here lets us keep a clean exc chain
            pass

        try:
            return dict.__getitem__(self, EthAddressKey(key))
        except KeyError as e:
            raise exceptions.KeyError(*e.args) from e.__cause__

    def __setitem__(self, key: AnyAddressOrContract, value: T) -> None:
        if key in self:
            # It is ~700x faster to perform this check and then skip the checksum if we find a result for this key
            dict.__setitem__(self, key, value)
        else:
            dict.__setitem__(self, EthAddressKey(key), value)

    def _getitem_nochecksum(self, key: EthAddressKey) -> T:
        """
        Retrieve an item without checksumming the key.

        This method can be used in custom subclasses to bypass the checksum
        process ONLY if you know it has already been done at an earlier point
        in your code.

        Args:
            key (EthAddressKey): The checksummed Ethereum address key.

        Examples:
            >>> d = ChecksumAddressDict()
            >>> key = EthAddressKey("0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB")
            >>> d._setitem_nochecksum(key, True)
            >>> d._getitem_nochecksum(key)
            True
        """
        return dict.__getitem__(self, key)

    def _setitem_nochecksum(self, key: EthAddressKey, value: T) -> None:
        """
        Set an item without checksumming the key.

        This method can be used in custom subclasses to bypass the checksum
        process ONLY if you know it has already been done at an earlier point
        in your code.

        Args:
            key (EthAddressKey): The checksummed Ethereum address key.
            value (T): The value to associate with the key.

        Raises:
            ValueError: If the key is not a valid Ethereum address.

        Examples:
            >>> d = ChecksumAddressDict()
            >>> key = EthAddressKey("0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB")
            >>> d._setitem_nochecksum(key, True)
            >>> d[key]
            True
        """
        if not key.startswith("0x") or len(key) != 42:
            raise ValueError(f"'{key}' is not a valid ETH address")
        dict.__setitem__(self, key, value)
