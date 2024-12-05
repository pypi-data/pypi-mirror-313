import hashlib


def create_file_hash(path: str) -> str:
    """
    Read file and return hash as string

    Args:
        path: path of the file to read
    """
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        # This is to prevent loading the entire file
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
