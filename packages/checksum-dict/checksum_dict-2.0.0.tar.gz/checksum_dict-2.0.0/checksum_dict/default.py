from typing import Callable, DefaultDict, Iterable

from checksum_dict._key import EthAddressKey
from checksum_dict.base import ChecksumAddressDict, T, _SeedT


class DefaultChecksumDict(DefaultDict[EthAddressKey, T], ChecksumAddressDict[T]):
    """
    A defaultdict that maps Ethereum addresses to objects.

    This class inherits from both :class:`collections.DefaultDict` and
    :class:`~checksum_dict.base.ChecksumAddressDict`. It will automatically
    checksum your provided address key when setting and getting values through
    the inherited behavior from :class:`~checksum_dict.base.ChecksumAddressDict`.

    Note:
        This implementation uses a :mod:`cchecksum`'s Cython implementation for checksumming to optimize
        performance over the standard :func:`eth_utils.to_checksum_address`.

    Example:
        >>> from checksum_dict import DefaultChecksumDict
        >>> default = int
        >>> d = DefaultChecksumDict(default)
        >>> lower = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"
        >>> print(d[lower])
        0
        >>> d[lower] = 42
        >>> print(d[lower])
        42

    As shown, the lowercase key `lower` is automatically checksummed when
    setting and getting values.

    See Also:
        - :class:`~checksum_dict.base.ChecksumAddressDict`
        - :class:`collections.DefaultDict`
        - :class:`EthAddressKey` for details on how keys are checksummed.
    """

    def __init__(self, default: Callable[[], T], seed: _SeedT = None) -> None:
        super().__init__(default)
        self.__dict__ = self
        if isinstance(seed, dict):
            seed = seed.items()
        if isinstance(seed, Iterable):
            for key, value in seed:
                self[key] = value

    def _getitem_nochecksum(self, key: EthAddressKey) -> T:
        """
        Retrieve an item without checksumming the key.

        This method can be used in custom subclasses to bypass the checksum
        process ONLY if you know it has already been done at an earlier point
        in your code.

        Example:
            >>> d = DefaultChecksumDict(int)
            >>> key = EthAddressKey("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
            >>> d._setitem_nochecksum(key, 100)
            >>> print(d._getitem_nochecksum(key))
            100

        See Also:
            - :meth:`~checksum_dict.base.ChecksumAddressDict._getitem_nochecksum`
        """
        if key in self:
            return self[key]
        default = self.default_factory()  # type: ignore
        self._setitem_nochecksum(key, default)
        return default
