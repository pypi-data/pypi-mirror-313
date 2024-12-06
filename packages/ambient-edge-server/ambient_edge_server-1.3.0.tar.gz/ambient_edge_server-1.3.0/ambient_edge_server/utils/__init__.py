import hashlib


def hash_string(input_string: str) -> str:
    # Create a new sha256 hash object
    hash_object = hashlib.sha256()

    # Encode the input string and update the hash object
    hash_object.update(input_string.encode("utf-8"))

    # Get the hexadecimal representation of the hash
    hashed_string = hash_object.hexdigest()

    return hashed_string
