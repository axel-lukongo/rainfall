# Level 0 - Binary Exploitation

## Introduction
In this level, we have a binary `level0`. When executed without any parameter, it causes a segmentation fault:

```bash
level0@RainFall:~$ ./level0
Segmentation fault (core dumped)
```

However, when we pass a parameter, it displays a message:

```bash
level0@RainFall:~$ ./level0 test
No !
```

This indicates that the binary expects a specific argument, likely a password.

## Analysis with Ghidra
To better understand its behavior, we use **Ghidra** to disassemble and analyze the binary code. Here is the `main` function obtained after reverse engineering:

```c
undefined4 main(int ac,char **av)
{
  int arg;
  char *argv;
  undefined4 local_1c;
  __uid_t euid;
  __gid_t egid;
  
  arg = atoi(av[1]);
  if (arg == 423) {
    argv = strdup("/bin/sh");
    local_1c = 0;
                    /* Get effective group id */
    egid = getegid();
                    /* Get effective user id */
    euid = geteuid();
                    /* Set effective, real and saved group id to level1 */
    setresgid(egid,egid,egid);
                    /* Set effective, real and saved user id to level1 */
    setresuid(euid,euid,euid);
    execv("/bin/sh",&argv);
  }
  else {
    fwrite("No !\n",1,5,(FILE *)stderr);
  }
  return 0;
}
```

### Code Explanation
1. The program converts the first argument to an integer using `atoi(av[1])`.
2. It compares this integer to `423`.
3. If the argument equals `423`:
   - It creates a copy of the string `"/bin/sh"`.
   - It retrieves the effective user (`euid`) and group (`egid`) IDs.
   - It uses `setresuid` and `setresgid` to change the UID/GID to those of `level1`.
   - It executes a shell (`/bin/sh`) using `execv()`.
4. If the argument is incorrect, it simply prints `No !`.

## Exploitation
Since this binary has the **SUID bit** set for `level1`, we can exploit this weakness to gain a shell with its privileges.

We execute the following command:

```bash
level0@RainFall:~$ ./level0 423
$ /bin/bash
bash: /home/user/level0/.bashrc: Permission denied
level1@RainFall:~$ 
```

Now, we are logged in with `level1` privileges!

## Retrieving the Next Level Password
The password for `level1` is stored in `/home/user/level1/.pass`. We can simply print it using:

```bash
level1@RainFall:/home/user/level1$ cat .pass
1fe8a524fa4bec01ca4ea2a869af2a02260d4a7d5fe7e7c24d8617e6dca12d3a
```

## Conclusion
This level demonstrates a common vulnerability related to **insecure SUID binaries**. By using `atoi()` without verifying the number of arguments and calling `execv()` with root access, the program becomes exploitable. A more secure implementation should include:
- Strict validation of the number of arguments.
- Proper user input validation.
- Avoiding execution of commands with elevated privileges without proper safeguards.

Thus, we successfully escalated our privileges to `level1` and retrieved the password for the next level. 🎯

