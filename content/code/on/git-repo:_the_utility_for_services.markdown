---
type: post
categories: code
tags: [ python, code, github, gitlab, bitbucket, git ]
title: Git-Repo The ultimate utility for managing services
date: 2016-10-10T16:15:14+02:00
summary: "There are many online platform offering repository hosting, though they all suck at one thing, it's to integrate nicely in the flow of coding. Some have a GUI tool, others integrate more or less in your editor (or IDE), and that's rarely the ones you're using for your work. After the break, let me show you my take on this, with a little tool I wrote called `git-repo`…"
lang: english
logo: /img/gitlogo-black.png 
header_background: /img/gitdark-bg.png 
tweet: 785496102313140226
---

Over the last decade, we've seen many online platform offering repository hosting,
like SourceForge, Savannah, Gitorious, Google Code, Github, Launchpad, Gitlab… And
a bunch of others I fail to remember. They offer a great service to help developers
and the FLOSS community to make it easy to find and share code on a project.

Though, they all always sucked at one thing, it's to integrate nicely in the flow
of coding. Some have a GUI tool, others integrate more or less in your editor (or
IDE), and that's rarely the ones you're using for your work.

The git utility has a rather well designed interface to make it easy to remember,
extend, and/or customize. So, out of frustration of having to swing between my code
and a web-page to issue some actions on a repository. I figured I could write a tool
to exploit those services APIs and make their features available where they belong,
in your shell!

# The problem

Let's say you've discovered a super neat python project you've installed and
love, that's called `foobar`. You've installed it using `pip` from `pypi`. Then
you've discovered a bug in that project, and want to fix it. So you do `pip
info foobar` (or the same with `npm`, `gems`…) to see its repository:
`https://github.com/ford_prefect/foobar.git`.

Then, you check it out, with: 

``` shell
git clone https://github.com/ford_prefect/foobar.git
```
then you watch the code, create a branch:

``` shell
git checkout -b `bugfix/nasty_one`
```

fix it, update the tests, and install it locally, and then you've got an updated
version of the code on your machine. Nothing out of ordinary here, that's how life works…

…At least as long as you're not the sharing type. Otherwise, you know you've
got to contribute your patch back to the community, by sending a patch on the
repository. 

But it's not [as simple as doing a `git format-patch` and mailing it](https://www.wired.com/2012/05/torvalds_github/), why would it?

Nah, you need to:

* open your browser on github, at the `https://github.com/ford_prefect` page, and 
* click on the little `fork` button:

![](img/git-fork.jpg)

Then once the repository added, you have to change the remotes, so yours is the
origin and the other one the upstream:

``` bash
% git remote origin set-url https://github.com/your_name/foobar.git
% git remote add upstream https://github.com/ford_prefect/foobar.git
```

(which nobody does, because who remembers the `git remote` syntax?

That being done, you then got to push your branch onto your remote, as a new branch.
Then, you have to open your browser and *click* on the create pull request button.

![](img/git-pull-request.png)

And then, only then, the original author will get notified of your change and will
be able to review your patch, and eventually integrate it.

So basically, you've got to switch between your editor, the browser and the
command-line, and do like five operations across those, where you really meant
to do three actions. And then, what about pushing that code to gitlab? Or
bitbucket?

# The solution

Over the last ten years, I always found each time I was doing those actions, I was
being frustrated by having to do those useless operations, and wanted to do something
to get rid of those.

I eventually did:

> https://github.com/guyzmo/git-repo

Now, what I'm doing for the same thing as above is:

``` bash
% git hub clone ford_prefect/foobar
% # hack, hack, hack!
% git co -b 'bugfix/nasty_one'
% git hub fork
% git push github bugfix/nasty_one
% git hub request create 'Fixed a nasty bug' --message 'Fixing issue with the thing'
```

And *voilà*! 🙌

If you want to create a repository on Gitlab, and push the code base over there? Well, easy:

``` bash
% git lab create foobar
% git push gitlab master
```

As an extra, if while you're debbuging you're running into an unreadable stacktrace
or compilation error:

``` bash
% git hub gist create 'Awful compilation error… Help me out' compilation.log
```

And of course, once your output is made irrelevant, you can simply delete it by doing a:

``` bash
% git hub gist delete https://gist.github.com/XXXXXXXXXXX
```

where the `X`s matches the gist to get rid of. And you have `git hub gist ls` that lists
all your gists!

# Choices made

Because everybody can manage their Git repository the way they prefer,
I decided that git-repo would never ever mingle with the `origin` remote. The
`origin` branch is a special git convention that can change the behaviour of
other tools, so it's better left in the hand of the user!

Another reason for `git-repo` to not decide what `origin` is, is that the tool
is made so it does not favour a service over another one, thus it makes a lot
more sense to have each service have a custom label (`gitlab`, `github`…).

Then one could consider using `origin` as the base remote for the fork. But I believe
that would be wrong as well, because in git convention, the `origin` is the remote
you're working with, and the upstream is most of the time read only. Which is why
the upstream is kept as the `upstream` branch.

Finally, git-repo comes with a nice hack: the `all` branch. When you have several
services configured as a remote for your current repository, they are as well configured
as a single branch target: the `all` branch. So when you do:

``` bash
% git push all master
```

You're pushing the branch master on all your remotes at once! So of course it's no
magic and you'll need to synchronize your local remote indexes (using `git fetch --all`)
so they're kept up to date with the different remotes, but it's easier than doing as
many pushes as you have remotes!

# Status of the project

For your first time run, I have written a wizard, that you can lanuch using:

``` bash
% git-repo config
```

and will update your `~/.gitconfig` with the relevant configuration details, and
define the aliases so you can call `git-repo` as `git lab` or `git hub`…

As a final word, this is the first published version, and the second prototype
I wrote (thus the `1.x` version scheme). I consider it being still in a *beta*
phase as I still believe the CLI API ergonomy for all the commands is still
perfectible so they feel natural to type and remember. That's the reason why
I did not split the project into submodules, and we have this huge help screen
that has it all.

To know more about the tool, you might want to check a series of screencasts I wrote:

1. [New project](https://asciinema.org/a/86e5sa1m03lwfiq0r0vwulvef)
2. [Delete project](https://asciinema.org/a/5xswp3wohdnc5xcr59t07fipj)
3. [Fork a project! 🍴](https://asciinema.org/a/f2apf8yencigbeznli87jn4lh)
4. [Got PR? 👋](https://asciinema.org/a/f2apf8yencigbeznli87jn4lh)
5. [Wanna gist with me? 📎](https://asciinema.org/a/cpjuxczprkihw3ssa23cummwb)
6. [⑥ There's more to gist! 📎](https://asciinema.org/a/6t24u8pdx7y7nmwmdb7vfgr5l)

I'd be happy to have some feedback either on twitter or on the [Github issues](https://github.com/guyzmo/git-repo/issues). 
