# What is a call stack ?

Call stack is what allows for functional programming well to function (😂) ...
It's what allows us to do 3 things :
- Know where to return once the function calls the `ret` instruction ie. the return instruction pointer.
- It allows us to store local variables for each function call.
- It allows us to pass parameters to functions.

In order to do so, we'll use a LIFO structure (a stack). Each component of the stack is called the **stack frame** and corresponds to what we've seen above.
```text
rsp-> +-------------locals------------+
      | 0x00 - 0x14 | int a           |
      | 0x10 - 0x60 | char buff[0x50] |
      +-------------return------------+
      | 0x60 - 0x64 | rip             |
      +-------------params------------+
      | 0x64 - 0x70 | int arg         |
      +-------------locals------------+
      | 0x00 - 0x14 | int a           |
      | 0x10 - 0x60 | char buff[0x50] |
      +-------------return------------+
      | 0x60 - 0x64 | rip             |
      +-------------params------------+
      | 0x64 - 0x70 | int arg         |
      +-------------+-----------------+
                    .
                    .
                    .
```

Everytime, we use `call` to call a function, a stack frame is added to the top of the stack which is pointed `rsp` register.

And that's it, so simple yet incredibly useful.