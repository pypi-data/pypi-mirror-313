# rpmdb/endian.py


def byte_order(swapped: bool) -> str:
    return ">" if swapped else "<"
