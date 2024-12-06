def evm_address_to_bytes(address: str | bytes) -> bytes:
    bytes_address = None
    if isinstance(address, bytes):
        bytes_address = address
    elif isinstance(address, str) and (address.startswith("0x") or address.startswith("0X")):
        address = address[2:]
        bytes_address = bytes.fromhex(address)
    else:
        raise ValueError("Invalid address")
    
    if len(bytes_address) != 20:
        raise ValueError(f"Invalid address length: expected 20 bytes, but got {len(bytes_address)} bytes")
    
    return bytes_address

def evm_from_bytes(bytes_address: bytes) -> str:
    return f"0x{bytes_address.hex()}"
