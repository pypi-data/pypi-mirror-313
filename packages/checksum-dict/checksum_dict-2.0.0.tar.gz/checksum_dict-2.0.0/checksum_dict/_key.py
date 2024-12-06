# type: ignore
import binascii
from typing import TYPE_CHECKING, Type, TypeVar, Union, cast, overload

from cchecksum import to_checksum_address
from eth_typing import AnyAddress
from eth_utils import add_0x_prefix


if TYPE_CHECKING:
    import brownie
    import y

    AnyAddressOrContract = TypeVar("AddressOrContract", "AnyAddress", brownie.Contract, y.Contract)


class EthAddressKey(str):
    """
    A string subclass that represents a checksummed Ethereum address.

    This class ensures that Ethereum addresses are stored in a checksummed format,
    which is crucial for preventing errors due to mistyped addresses.

    Note:
        This implementation uses a custom Cython function for checksumming to optimize
        performance over the standard :func:`eth_utils.to_checksum_address`.

    Examples:
        Create a checksummed Ethereum address from a string:

        >>> address = EthAddressKey("0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        >>> print(address)
        '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'

        Create a checksummed Ethereum address from bytes:

        >>> address_bytes = bytes.fromhex("b47e3cd837ddf8e4c57f05d70ab865de6e193bbb")
        >>> address = EthAddressKey(address_bytes)
        >>> print(address)
        '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'

    Raises:
        ValueError: If the provided value cannot be converted to a valid Ethereum address.

    See Also:
        - :func:`eth_utils.to_checksum_address` for the standard checksum conversion.
        - :func:`checksum_dict.checksum.to_checksum_address` for our implementation.
    """

    def __new__(cls, value: Union[bytes, str]) -> str:
        if isinstance(value, bytes):
            converted_value = (
                value.hex() if type(value).__name__ == "HexBytes" else HexBytes(value).hex()
            )
        else:
            converted_value = add_0x_prefix(str(value))
        try:
            converted_value = to_checksum_address(converted_value)
        except ValueError as e:
            raise ValueError(f"'{value}' is not a valid ETH address") from e
        return super().__new__(cls, converted_value)


"""
This library was built to have minimal dependencies, to minimize dependency conflicts for users.
The following code was ripped out of eth-brownie on 2022-Aug-06.
A big thanks to the many maintainers and contributors for their valuable work!
"""


def to_bytes(val: Union[bool, bytearray, bytes, int, str]) -> bytes:
    """
    Convert a value to its bytes representation.

    This function is equivalent to `eth_utils.hexstr_if_str(eth_utils.to_bytes, val)`.
    It can convert a hex string, integer, or boolean to a bytes representation.
    Alternatively, it passes through bytes or bytearray as a bytes value.

    Args:
        val: The value to convert, which can be a bool, bytearray, bytes, int, or str.

    Raises:
        ValueError: If the integer is negative.
        TypeError: If the value is of an unsupported type.

    Examples:
        Convert a hex string to bytes:

        >>> to_bytes("0x1234")
        b'\x124'

        Convert an integer to bytes:

        >>> to_bytes(4660)
        b'\x124'

        Convert a boolean to bytes:

        >>> to_bytes(True)
        b'\x01'
    """
    if isinstance(val, bytes):
        return val
    elif isinstance(val, str):
        return hexstr_to_bytes(val)
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, bool):
        return b"\x01" if val else b"\x00"
    elif isinstance(val, int):
        # Note that this int check must come after the bool check, because
        #   isinstance(True, int) is True
        if val < 0:
            raise ValueError(f"Cannot convert negative integer {val} to bytes")
        else:
            return to_bytes(hex(val))
    else:
        raise TypeError(f"Cannot convert {val!r} of type {type(val)} to bytes")


def hexstr_to_bytes(hexstr: str) -> bytes:
    """
    Convert a hex string to bytes.

    Args:
        hexstr: The hex string to convert.

    Raises:
        ValueError: If the hex string contains invalid characters.

    Examples:
        Convert a hex string with a prefix:

        >>> hexstr_to_bytes("0x1234")
        b'\x124'

        Convert a hex string without a prefix:

        >>> hexstr_to_bytes("1234")
        b'\x124'
    """
    if hexstr.startswith("0x") or hexstr.startswith("0X"):
        non_prefixed_hex = hexstr[2:]
    else:
        non_prefixed_hex = hexstr

    # if the hex string is odd-length, then left-pad it to an even length
    if len(hexstr) % 2:
        padded_hex = "0" + non_prefixed_hex
    else:
        padded_hex = non_prefixed_hex

    try:
        ascii_hex = padded_hex.encode("ascii")
    except UnicodeDecodeError:
        raise ValueError(f"hex string {padded_hex} may only contain [0-9a-fA-F] characters")
    else:
        return binascii.unhexlify(ascii_hex)


class HexBytes(bytes):
    """
    A thin wrapper around the Python built-in :class:`bytes` class for handling hexadecimal bytes.

    This class provides additional functionality for initializing with various types and
    representing the bytes in a hexadecimal format with a '0x' prefix.

    Examples:
        Create a HexBytes object from a hex string:

        >>> hb = HexBytes("0x1234")
        >>> print(hb)
        HexBytes('0x1234')

        Create a HexBytes object from an integer:

        >>> hb = HexBytes(4660)
        >>> print(hb)
        HexBytes('0x1234')

    See Also:
        - :func:`to_bytes` for converting various types to bytes.
    """

    def __new__(cls: Type[bytes], val: Union[bool, bytearray, bytes, int, str]) -> "HexBytes":
        bytesval = to_bytes(val)
        return cast(HexBytes, super().__new__(cls, bytesval))  # type: ignore  # https://github.com/python/typeshed/issues/2630  # noqa: E501

    def hex(self) -> str:
        """
        Output hex-encoded bytes, with an "0x" prefix.

        Everything following the "0x" is output exactly like :meth:`bytes.hex`.

        Examples:
            >>> hb = HexBytes("0x1234")
            >>> hb.hex()
            '0x1234'
        """
        return "0x" + super().hex()

    @overload
    def __getitem__(self, key: int) -> int: ...

    @overload  # noqa: F811
    def __getitem__(self, key: slice) -> "HexBytes": ...

    def __getitem__(self, key: Union[int, slice]) -> Union[int, bytes, "HexBytes"]:  # noqa: F811
        result = super().__getitem__(key)
        if hasattr(result, "hex"):
            return type(self)(result)
        else:
            return result

    def __repr__(self) -> str:
        return f"HexBytes({self.hex()!r})"
