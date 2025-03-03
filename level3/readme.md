# Level3

## Information gathering

No security, yadi yadi ya. We send it to ghidra, we get this pseudo-C :

```c
void v(void)

{
  char local_20c [520];
  
  fgets(local_20c,0x200,stdin);
  printf(local_20c);
  if (m == 0x40) {
    fwrite("Wait what?!\n",1,0xc,stdout);
    system("/bin/sh");
  }
  return;
}
```

WTF !? We control the format argument of the printf function call. This is very sus ඞ !!!!

We can supply things like `%p %s` and it will leak values on the stack. And we can also write things with the `%u` which writes the number of characters written so far to the next argument.

## Exploitation

```text
id
uid=2022(level3) gid=2022(level3) euid=2025(level4) egid=100(users) groups=2025(level4),100(users),2022(level3)
```

```text
cat /home/user/level4/.pass
b209ea91ad69ef36f2cf0fcbbc24c739fd10464cf545b20bea8572ebdc3c36fa
```

## References

- [Lecture Notes (Syracuse University), Format String Vulnerability](https://web.ecs.syr.edu/~wedu/Teaching/cis643/LectureNotes_New/Format_String.pdf) 