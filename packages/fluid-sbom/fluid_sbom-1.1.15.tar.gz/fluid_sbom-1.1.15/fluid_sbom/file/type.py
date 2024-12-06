from enum import (
    Enum,
)
from tarfile import (
    TarInfo,
)


class Type(Enum):
    TYPE_REGULAR = "TypeRegular"
    TYPE_HARD_LINK = "TypeHardLink"
    TYPE_SYM_LINK = "TypeSymLink"
    TYPE_CHARACTER_DEVICE = "TypeCharacterDevice"
    TYPE_BLOCK_DEVICE = "TypeBlockDevice"
    TYPE_DIRECTORY = "TypeDirectory"
    TYPE_FIFO = "TypeFIFO"
    TYPE_SOCKET = "TypeSocket"
    TYPE_IRREGULAR = "TypeIrregular"


def get_type_from_tar_member(  # noqa: PLR0911
    member: TarInfo,
) -> Type:
    if member.issym():
        return Type.TYPE_SYM_LINK
    if member.islnk():
        return Type.TYPE_HARD_LINK
    if member.isreg():
        return Type.TYPE_REGULAR
    if member.isdir():
        return Type.TYPE_DIRECTORY
    if member.isfifo():
        return Type.TYPE_FIFO
    if member.ischr():
        return Type.TYPE_CHARACTER_DEVICE
    if member.isblk():
        return Type.TYPE_BLOCK_DEVICE
    return Type.TYPE_IRREGULAR
