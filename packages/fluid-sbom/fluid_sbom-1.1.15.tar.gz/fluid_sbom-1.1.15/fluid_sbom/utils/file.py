import tarfile
from contextlib import (
    suppress,
)

from pydantic import (
    BaseModel,
    Field,
)

# IEC Sizes
BYTE = 1 << (0 * 10)
KIBYTE = 1 << (1 * 10)
MIBYTE = 1 << (2 * 10)
GIBYTE = 1 << (3 * 10)
TIBYTE = 1 << (4 * 10)
PIBYTE = 1 << (5 * 10)
EIBYTE = 1 << (6 * 10)

# SI Sizes
IBYTE = 1
KBYTE = IBYTE * 1000
MBYTE = KBYTE * 1000
GBYTE = MBYTE * 1000
TBYTE = GBYTE * 1000
PBYTE = TBYTE * 1000
EBYTE = PBYTE * 1000

bytes_size_table = {
    "b": BYTE,
    "kib": KIBYTE,
    "kb": KBYTE,
    "mib": MIBYTE,
    "mb": MBYTE,
    "gib": GIBYTE,
    "gb": GBYTE,
    "tib": TIBYTE,
    "tb": TBYTE,
    "pib": PIBYTE,
    "pb": PBYTE,
    "eib": EIBYTE,
    "eb": EBYTE,
    # Without suffix
    "": BYTE,
    "ki": KIBYTE,
    "k": KBYTE,
    "mi": MIBYTE,
    "m": MBYTE,
    "gi": GIBYTE,
    "g": GBYTE,
    "ti": TIBYTE,
    "t": TBYTE,
    "pi": PIBYTE,
    "p": PBYTE,
    "ei": EIBYTE,
    "e": EBYTE,
}


def parse_bytes(size_human: str) -> int:
    # Initialize the last digit index and the flag for comma presence
    last_digit = 0
    has_comma = False

    # Identify the last digit or comma in the string
    for i, char in enumerate(size_human):
        if not (char.isdigit() or char in {".", ","}):
            break
        if char == ",":
            has_comma = True
        last_digit = i + 1

    # Extract the number part and remove commas if present
    num_str = size_human[:last_digit]
    if has_comma:
        num_str = num_str.replace(",", "")

    # Convert the number string to float
    try:
        num = int(num_str)
    except ValueError as exc:
        error_message = f"Could not parse number: {num_str}"
        raise ValueError(error_message) from exc

    # Get the unit and calculate the final value
    extra = size_human[last_digit:].strip().lower()
    if extra in bytes_size_table:
        num *= bytes_size_table[extra]
        return num

    error_message = f"Unhandled size name: {extra}"
    raise ValueError(error_message)


def extract_tar_file(tar_path: str, out_path: str) -> None:
    with tarfile.open(tar_path, "r") as tar:
        for member in tar.getmembers():
            member.name = member.name.lstrip("/")
            with suppress(Exception):
                tar.extract(member, path=out_path)


class Digest(BaseModel):
    algorithm: str | None = Field(min_length=1)
    value: str | None = Field(min_length=1)
