---
type: post
categories: code
tags: [ python, code, docopt ]
title: Docopt, the elegant way to build CLI
date: 2016-11-01T15:43:22+02:00
summary: "Recently I have been caught in a troll with a friend who told me he
dislikes docopt, and prefers to stick with argparse. Ever since I started using
docopt, I love it and see no reason to stop using it. So we'll see why after the break…"
lang: english
logo: /img/docopt.png
header_background: /img/docopt_cli.jpg
tweet: 796018573793599488
---

Recently, I've been caught in a troll [with a friend who told me he doesn't
like `docopt`][1] and prefers to stick with `argparse`.

[1]:https://dmerej.info/blog/post/docopt-v-argparse/

<center>
[![](/img/duty_calls.png)][duty-calls]
</center>

[duty-calls]:https://www.xkcd.com/386/

My opinion is that both are just *tools* with strong and weak points. I do have
a preference over defaulting to `docopt`, and use something else really when I'm
hitting a use case that makes docopt totally irrelevent.

# CLI Design

I don't think there's such a thing as a *simple* CLI or a *complex* CLI, because the
number of arguments does not necessarily affects the complexity of the interface,
the issue would mostly be how well is it exposed and documented so it is made easy
to *use*.

I prefer to think in terms of usage. I believe there are two main approaches to
CLI design. Either, it's a complement to configuring the environment before
starting a long running application (whether it is a service, a GUI, a webapp
or an REPL), or it's a tool meant to integrate in one user's shell toolbox,
where the CLI is the main interface.

# KISS and DRY design

In the first case, your main focus is on the code itself, and not really on the
arguments, so writing an argument handler and doing a start at documenting your
app is done in a single action when you're building your application.

``` python

'''
Usage: myapp [options]

Arguments:
  -c,--config=<file>       Sets up configuration file [default: myconf.yaml]
  -v,--verbose             Enable verbose output
  -h,--help		   This page

This is a tool to demonstrate that it takes less than a minute to setup a flexible,
readable and documented CLI for any kind of app.
'''

from docopt import docopt

def main():
   args = docopt(__doc__)

   # start your app with the default configurations
   my_app(
      config=args['--config'],
      verbose=args['--verbose']
   )

```

And then you can focus on actually coding whatever `my_app()` is doing, which
is what you should be focused on. If you want to add a log option, you'd update
only `__doc__` with the matching line, and add it as a new argument in the
`my_app()` call.

There your CLI parsing code is readable, showing only the essential, yet flexible
enough to adapt to your needs so you're always building up a CLI that makes the
tool you're building looking alike every other Unix tool.

# More advanced CLI design

For small applications, checking arguments by looking at the dictionary is really
nice way, because it keeps things simple and easy to read.

For more complex applications, where the CLI is the main point of interaction with
the user, you will want to build an interface that has more arguments, and thus more
possibilities in combining those arguments. And that's ok, because some programs are
meant to provide almost a "custom" language to make using them nice.

There, using docopt the traditional way will get your cyclometric complexity through
the roof… like:

```
if args['command']:
   if args['--input']:
      if args['--accept']:
	 if args['--number']:
	    try:
	       n = int(args['--number'])
	    except:
	       print("Error!")
	 else:
	    # …
```

It's actually the other side of the coin when having a very straightforward approach
to CLI parsing, and it's ok, because replacing a chaos of conditional with a more
declarative approach is nothing new. You can write your own command dispatcher [like I did for git-repo][2]

[2]:https://github.com/guyzmo/git-repo/blob/master/git_repo/kwargparse.py

Or be smarter than I was, and use the already existing [docopt-dispatch][3] which would
deserve more credit:

```
from docopt_dispatch import dispatch

@dispatch.on('command', '--input', '--accept', '--number')
def do_command_input_accept_number(cmd, input, accept, number):
   try:
      n = int(number)
   except:
      print("Error!")
```

[3]:https://github.com/keleshev/docopt-dispatch

# When docopt is not great, something's wrong with your design

The only time I really reached the possibilities of what I could do with docopt was
when I wanted to implement a configuration file that's modifying how the CLI will
behave.

It's actually possible to do this with docopt, but you'll end up having a configuration
split in two parts and the second part being filled with `{}` format strings so that
when reading the `__doc__` or the source code, it's becoming unreadable.

Doing so is definitely much simpler with something like `argparse`… But as I was
trying to hack my way through that… I realized how wrong that was. The CLI should
*always* override the configuration values, and the configuration override the default
values. That's the expected order of precendence, and doing it another way would be
breaking an expected behaviour of any Unix software.

# Docopt behaves the same way in other languages

When I needed to build a quick hack in C++ to test usage of a library, then the
commandline is definitely not the important part. Back at uni, for that kind of
code I used to either do it myself and make pretty ugly CLI, because I did not
want to spend time on the parser (so basically iterating over the options from
the end of the `argv` array), or use [`getopt`][4].

[4]:https://www.gnu.org/savannah-checkouts/gnu/libc/manual/html_node/Getopt.html

Other options might be to use [boost argument parser][5], or decide [which][6] [one][7]
you want. And you don't always get a great looking CLI help page.

[5]:http://www.boost.org/doc/libs/1_62_0/doc/html/program_options.html
[6]:http://tclap.sourceforge.net/
[7]:http://optionparser.sourceforge.net/index.html

With [docopt.cpp][8], you can parse your code nicely. With a bit more complexity and
increasing the size of your build… But it's a thing you run only once at start of your
app, and it's still faster than spawning a process.

[8]:https://github.com/docopt/docopt.cpp

# Yeah, I'm sticking with docopt

So, whatever better feature another argument parsing library has, I prefer to stick
with docopt. Yes, it's lacking type checking (though [a patch][9] tries to fix that),
it's not bundled with the language (but like many other great libraries like `requests`),
and error reporting could be improved (another [patch][10]).

[9]:https://github.com/docopt/docopt/pull/334
[10]:https://github.com/docopt/docopt/pull/63

But what other tools lack is the flexibility to craft your own help message so it's
actually part of the documentation and not some ugly and hard to understand bit of
technicality that forces you to go read the README before using the program.



