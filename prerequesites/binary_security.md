## What is a stack canary ?

A stack canary is inspired by the canaries used to protect miners from toxic gases. Before modern gas detection technology, miners would carry a caged canary into the mine. Since canaries are more sensitive to dangerous, odorless gases, their death served as an early warning for miners to evacuate.

Stack canaries rely on the same concept, we put a randomly initalized and secret value in the stack and if it changes, we know that a buffer overflow has occured and we can terminate the program before the harm is done.

Here's an example, of what the stack frame would look like.

```text
      +-------call to swap----------+
rsp ->+-------------locals------------+
      | 0x00 - 0x14 | int a           |
      | 0x10 - 0x60 | char buff[0x50] |
      +-------------------------------+
      |         64bit canary          |
      +-------------return------------+
      | 0x60 - 0x64 | addr            |
      +-------------params------------+
      | 0x64 - 0x70 | int arg         |
      ---------------------------------
                    .
                    .
                    .
```

Here, if we overflow buffer, we'd have to overwrite the canary first in order to overwrite the return variable.

## What is NX ?

NX stands for Non-eXecutable stack and it is just making the stack not executable.

## What is ASLR ?

ASLR stands for Address Space Layout Randomization, and it allows the program to be loaded in memory at a different offset each time we run it, which makes exploitation harder.

## What is RELRO ?

