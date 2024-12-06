from typing import final


@final
class KeyError(KeyError):
    def __repr__(self) -> str:
        return f"<checksum_dict.KeyError({str(self)})>"
