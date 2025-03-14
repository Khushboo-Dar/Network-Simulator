def checksum(data):
    return sum(bytearray(data, 'utf-8')) % 256

def verify_checksum(data, received_checksum):
    return checksum(data) == received_checksum
