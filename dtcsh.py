#!/usr/bin/env python -tt

"""
This module implements a python interface for dtcsh.
"""


import subprocess


class DTCShError(Exception):

    """
    Can be raised by DTCSh.check_result
    Contains dtcsh stderr and returncode.
    """

    def __init__(self, stderr, returncode):
        Exception.__init__(self)
        if stderr:
            self.stderr = stderr
        else:
            self.stderr = "<empty stderr>"
        self.returncode = returncode

    def __str__(self):
        return "exit {0}: {1}".format(self.returncode, self.stderr)


class DTCSh(subprocess.Popen):

    """
    A subprocess.Popen running dtcsh, with specific attributes:
    * stdout and stderr are subprocess.PIPEs
    * __init__ shell parameter is False.

    __init__ arguments are dtcsh arguments, as a list of strings. The
    first one should be a valid dtcsh subcommand.
    """

    subcommands = ['ls', 'cat', 'match', 'grep', 'whatever']

    def __init__(self, *args):
        if len(args) < 1:
            raise ValueError("Not enough parameters.")
        if args[0] not in self.subcommands:
            raise ValueError("%s: not a valid dtcsh subcommand" % args[0])
        command_line = ['dtcsh']
        command_line.extend(args)
        subprocess.Popen.__init__(
            self, command_line, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=False)

    @classmethod
    def check_result(cls, subcommand, *args):
        """
        Create a DTCSh instance and return line-splited stdout if
        return code was 0. Else raise DTCShError.
        @param subcommand a valid dtcsh subcommand
        @params args a list of parameters
        @return a list matching re-tokenized dtcsh stdout.
        """
        dtc = cls(subcommand, *args)
        stdout, stderr = dtc.communicate()
        if dtc.returncode != 0:
            raise DTCShError(stderr, dtc.returncode)
        # Ensure the process wont appear in the process table anymore.
        del dtc
        return stdout.splitlines()


# We try to verify dtcsh can actually be executed.
try:
    DTCSh('grep', '.').communicate()
except OSError:
    print "Cannot execute the dtcsh command, please check your installation."
    raise
