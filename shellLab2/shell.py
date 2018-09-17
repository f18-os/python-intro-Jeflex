# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 12:49:13 2018

@author: Phillip
"""

import sys
import re
import os
import subprocess


while(1):
    sys.stdout.write(os.curdir + '$')
    # args = str(sys.stdin.readline().strip('\n').split(' '))
    args = input('').split(' ')
    if 'exit' == args[0]:
        break
    #if '>' in args:

    #if '<' in args:
    pid = os.getpid()
    if '|' in args:
        ind = args.index('|')

        argsPiped = args[ind - 1 : ]
        print(argsPiped)

        os.write(1, ("About to fork for pipe (pid=%d)\n" % pid).encode())

        rc = os.fork()

        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:
            os.write(1, ("PipeChild: My pid==%d.  Parent's pid=%d\n" %
                         (os.getpid(), pid)).encode())

            os.close(1)
            sys.stdout = open("outputForked.txt", "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd, True)
            os.write(2, ("PipeChild: opened fd=%d for writing\n" % fd).encode())
            argsPiped.remove('|')
            hold = argsPiped[0]
            argsPiped.remove(argsPiped[0])
            argsPiped.append(hold)
            
            if '/' in argsPiped[0]:
                try:
                    os.execve(argsPiped[0], argsPiped, os.environ)
                except:
                    pass
            else:
                for dir in re.split(":", os.environ['PATH']):
                    program = "%s/%s" % (dir, argsPiped[0])
                    try:
                        ret = os.execve(program, argsPiped, os.environ)
                        for a in argsPiped:
                            args.remove(a)
                        args.remove('|')
                        args.add(ret)
                    except FileNotFoundError:
                        pass

            os.write(2, ("PipeChild:    Error: Could not exec %s\n" % argsPiped[0]).encode())
            sys.exit(1)

        else:
            os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                         (pid, rc)).encode())
            childPidCode = os.wait()
            os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
        childPidCode).encode())


# resume
    pid = os.getpid()

    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

    rc = os.fork()
    print("began bottom fork")
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:
        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                     (os.getpid(), pid)).encode())

        os.close(1)
        sys.stdout = open("output.txt", "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

        if '/' in args[0]:
            try:
                os.execve(args[0], args, os.environ)
            except:
                pass
        else:
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ)
                except FileNotFoundError:
                    pass

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)

    else:
        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                     (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
    childPidCode).encode())
