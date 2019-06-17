# dtcsh
DSH with patterns, regexps.

# What is it ?

`dtcsh` is a wrapper for
[the dancer shell](https://www.netfort.gr.jp/~dancer/software/dsh.html.en). It
allows user to specify host names by regular expressions, or specify
group names by pattern

It's technically safe to do
```bash
alias dsh=dtcsh
```

However, it still relies on the original dsh.

# How to install it ?

## Prerequisites

You need to install `zsh`, `dsh` and `cssh` first of all.

## dtcsh installation

Get (git clone, or copy) the `dtcsh` script from this repository, and place it somewhere in your `$PATH`.

## Configuration

Just use `dsh` configuration.

# DSH enhancements

Imagine you have multiple node00{1,2,3,...}.mydomain servers located in multiple group files and you want to contact them.

```bash
# Instead of 
$ dsh -m node001.mydomain -m node002.mydomain -m .... uptime
# Do this
dtcsh -m 'node[0-9]+.mydomain' uptime
```

Or if there's a pattern in group files :

```bash
# Instead of 
$ dsh -g 'prod/node' -g 'dev/node' uptime
# You can do this
$ dtcsh h -g '*/node' ls
```

# More features

## Search for group files
```bash
# All groups named node
$ dtcsh ls '**/node'
# All groups underneath prod subdir
$ dtcsh ls 'prod/**/*'
```

All zsh extended patterns are allowed

## Search for hostnames
```bash
# You want to look for all hostnames containing keyword john
$ dtcsh grep keyword
```

## cssh wrapping

For people fond of interactivity, `dtcsh` can combine dsh groups power
with [clusterssh](https://github.com/duncs/clusterssh/wiki).

```bash
# Open an interactive shell on every node.
$ dtcsh cssh 'node[0-9]+.mydomain'
```

## More

```bash
$ dtcsh -h
DTCsh-wrapped Distributed Shell / Dancer's shell version 0.25.10 
Copyright 2001-2005 Junichi Uekawa, 
distributed under the terms and conditions of GPL version 2

-v --verbose                   Verbose output
-q --quiet                     Quiet
-M --show-machine-names        Prepend the host name on output
-H --hide-machine-names        Do not prepend host name on output
-i --duplicate-input           Duplicate input given to dsh
-b --bufsize                   Change buffer size used in input duplication
-m --machine [machinename]     Execute on machine
-n --num-topology              How to divide the machines
-a --all                       Execute on all machines
-g --group [groupname]         Execute on group member
-f --file [file]               Use the file as list of machines
-r --remoteshell [shellname]   Execute using shell (rsh/ssh)
-o --remoteshellopt [option]   Option to give to shell 
-h --help                      Give out this message
-w --wait-shell                Sequentially execute shell
-c --concurrent-shell          Execute shell concurrently
-F --forklimit [fork limit]    Concurrent with limit on number
-V --version                   Give out version information

Alternative syntaxes in which none of the above options apply:

dtcsh ls 'group_pattern'

        Prints the dsh group names matching given pattern.

dtcsh cat 'group_pattern'

        Prints the (uniq) hostnames contained in dsh group names
        matching given pattern.

dtcsh match 'hostname_regexp' [ 'group' ]

        Prints dsh group names containing hostnames matching given 'grep
        -E'-styled regular expression. If given, 'group' represents the
        beginning of a dsh group name, restricting the research to that
        'group' tree.

dtcsh grep 'hostname_regexp' [ 'group' ]

        Same as the 'match' command, but prints matching host names (and
        not dsh groups) instead.

dtcsh cssh [ <cssh option> ... ] '[login@](group|file|regexp|hostname)[:port]'

        Acts like cssh. Parameters can be either dsh groups, file names,
        hostname regular expression pattern or plain host names, with
        optional '<username>@' prefix and optional ':<port number>'
        suffix.  If 'dtcsh' is called as 'cssh' or 'dcssh', 'dtcsh' acts
        as if called as 'dtcsh cssh'.

dtcsh clean-keys '(group|regexp|hostname)'

        Remove entries from your ~/.ssh/known_hosts file. Parameters can be
        either dsh groups, hostname or hostname regular expressions. The
        IP address will also be removed from the known_hosts file.

dtcsh update-keys '(group|regexp|hostname)'

        Like clean-keys action but also attempt to connect the expanded
        list of hostnames so that latest version of host keys will be
        re-added to the known_hosts file.

dtcsh remove 'regexp'

        Removes all hostnames matching given regular expression from dsh
        groups.

dtcsh whatever '(group|regexp|hostname)'

        Expands arguments into a list of host names, whatever their
        nature: group pattern, host name regular expression or plain host
        name. It's the exact same subroutines used in clean-keys,
        update-keys and in the cssh wrapper.

```
