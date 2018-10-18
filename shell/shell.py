# -*- coding: utf-8 -*-

import sys
import re
import os
import subprocess


while(1):
    try:
        # a = os.environ["PS1"].pop()
        # if a == '':
        #     sys.stdout.write(os.getcwd() + ' $')
        # else:
        #     sys.stdout.write(os.getcwd() + os.environ["PS1"])
        # args = str(sys.stdin.readline().strip('\n').split(' '))
        # if os.environ['PS1']:
        #     sys.stdout.write(os.getcwd() + os.environ['PS1'] )
        # else:
        sys.stdout.write(os.getcwd() + ' $')
        args = input('').split(' ')
        if 'exit' == args[0]:
            break
        elif '' == args[0]:
            continue
        elif 'cd' == args[0]:
            if args[1] == '..':
                a = str(os.getcwd()).split('/')
                b='/'
                for s in a[:len(a)-1]:
                    b = b +'/'+ s
                try:
                    os.chdir(b)
                except:
                    print('File path could not be found.')
            else:
                try:
                    os.chdir(args[1])
                except:
                    print('File path could not be found.')

        else:
            pid = os.getpid()

            if '<' in args:
                ind = args.index('<')


                os.write(1, ("About to fork for input redirect (pid=%d)\n" % pid).encode())

                rc = os.fork()

                if rc < 0:
                    os.write(2, ("fork failed, returning %d\n" % rc).encode())
                    sys.exit(1)

                elif rc == 0:
                    os.write(1, ("InRedirChild: My pid==%d.  Parent's pid=%d\n" %
                                 (os.getpid(), pid)).encode())

                    os.close(0)
                    sys.stdin = open(args[1], "w")
                    fd = sys.stdout.fileno()
                    os.set_inheritable(fd, True)
                    os.write(2, ("InRedirChild: opened fd=%d for writing\n" % fd).encode())

                    if '/' in args[0]:
                        try:
                            os.execve(args[0], args, os.environ)
                        except:
                            pass
                    else:
                        for dir in re.split(":", os.environ['PATH']):
                            program = "%s/%s" % (dir, args[0])
                            try:
                                ret = os.execve(program, args, os.environ)

                            except FileNotFoundError:
                                pass

                    os.write(2, ("InRedirChild:    Error: Could not exec %s\n" % args[0]).encode())
                    sys.exit(1)

                else:
                    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
                                 (pid, rc)).encode())
                    childPidCode = os.wait()

                    os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                childPidCode).encode())

            pid = os.getpid()
            if '|' in args:
                ind = args.index('|')

                os.write(1, ("About to fork for pipe (pid=%d)\n" % pid).encode())

                pr,pw = os.pipe()

                for f in (pr, pw):
                    os.set_inheritable(f, True)
                print("pipe fds: pr=%d, pw=%d" % (pr, pw))

                import fileinput

                print("About to fork (pid=%d)" % pid)

                rc = os.fork()

                if rc < 0:
                    print("fork failed, returning %d\n" % rc, file=sys.stderr)
                    sys.exit(1)

                elif rc == 0:                   #  child - will write to pipe
                    print('In pipe')
                    print("Child: My pid==%d.  Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
                    # args = ["wc", "p3-exec.py"]

                    os.close(0)                 # redirect child's stdout
                    os.dup(pw)
                    # sys.stdout = open(args[0],'w+')
                    for fd in (pr, pw):
                        os.close(fd)
                    # re = os.fork()
                    # if re < 0:
                    #     print("fork failed, returning %d\n" % re, file=sys.stderr)
                    #     sys.exit(1)
                    # if re == 0:s
                    if '/' in args[3]:
                        try:
                            os.execve(args[3], args, os.environ)
                        except:
                            pass
                    else:
                        for dir in re.split(":", os.environ['PATH']):
                            program = "%s/%s" % (dir, args[3])
                            try:
                                os.execve(program, args, os.environ)
                            except FileNotFoundError:
                                pass
                    sys.exit(1)
                else:                           # parent (forked ok)
                    print('Out pipe')
                    print("Parent: My pid==%d.  Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
                    os.close(1)
                    os.dup(pr)
                    for fd in (pw, pr):
                        os.close(fd)
                    # for line in fileinput.input():
                    #     print("From child: <%s>" % line)


        # resume
            else:
                pid = os.getpid()

                # os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
                #
                # rc = os.fork()
                # print("began bottom fork")
                # if rc < 0:
                #     os.write(2, ("fork failed, returning %d\n" % rc).encode())
                #     sys.exit(1)
                #
                # elif rc == 0:
                #     os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
                #                  (os.getpid(), pid)).encode())
                #
                #     os.close(1)
                sys.stdout = open("output.txt", "w")
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                # os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

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

        # else:
        #     os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
        #                  (pid, rc)).encode())
        #     childPidCode = os.wait()
        #     os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
        # childPidCode).encode())
    except EOFError:
        break
