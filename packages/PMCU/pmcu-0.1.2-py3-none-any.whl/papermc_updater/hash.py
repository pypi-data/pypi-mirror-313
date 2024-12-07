import hashlib


def hasher(filename, size):
    global file_hash
    file: str = filename  # Location of the file
    BLOCK_SIZE = 131072  # The size of each read from the file

    if size == 256:
        file_hash = hashlib.sha256()
    elif size == 512:
        file_hash = hashlib.sha512()

    with open(file, 'rb') as f:  # Open the file to read its bytes
        fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
        while len(fb) > 0:  # While there is still data being read from the file
            file_hash.update(fb)  # Update the hash
            fb = f.read(BLOCK_SIZE)  # Read the next block from the file

    return str(file_hash.hexdigest())
