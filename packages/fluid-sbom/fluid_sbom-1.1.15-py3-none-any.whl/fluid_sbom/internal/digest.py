import hashlib
from io import (
    BufferedReader,
)

from fluid_sbom.utils.file import (
    Digest,
)


def new_digests_from_file(file_object: BufferedReader, hashes: list[str]) -> list[Digest]:
    # Create hash objects
    hash_objects = [hashlib.new(hash_key, usedforsecurity=False) for hash_key in hashes]

    # Read file and update each hash object
    while chunk := file_object.read(4096):
        for hasher in hash_objects:
            hasher.update(chunk)

    # Prepare the result list of Digest objects
    if file_object.tell() == 0:  # Check if file size is zero
        return []

    return [
        Digest(
            algorithm=hash_name,
            value=hasher.hexdigest(),
        )
        for hash_name, hasher in zip(hashes, hash_objects, strict=False)
    ]
