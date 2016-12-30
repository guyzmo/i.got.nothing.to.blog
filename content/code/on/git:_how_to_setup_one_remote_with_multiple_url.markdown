---
type: post
categories: code
tags: [ code, python, tip, git ]
title: "A tip for git, discover multiple URL remote"
date: 2016-12-30T20:28:42+02:00
summary: "While I was developing git-repo I stumbled upon a little known feature that
has been introduced in git 2.7: the possibility to have a remote with multiple
URLs. After the break I'll tell you what this is about…"
lang: english
logo: /img/gitlogo-black.png 
header_background: /img/gitdark-bg.png 
tweet: 814917694436868097
aliases: /code/on/git:_how_to_setup_one_url_with_multiple_remotes
---

While I was developing [git-repo] I stumbled upon a little known feature that
has been introduced in git 2.7: the possibility to have a remote with multiple
URLs.

# Why would I need that?

What's great with git is that it's a decentralized version control system. What that
means is that, even if most of the time you'll work with only one remote repository (in a
very centralised way), sometimes you'll be happy to be able to have many remotes to
work with.

An use case I had in a former work setup was to have an internal repository (that will
feature the open code, as well as some custom features in branches for our paying customers),
an external repository (because opensource is ♥), a production repository (for deployment
purposes, but it's not anymore a use case thanks to CI integrations that [does automatic
deployment](https://about.gitlab.com/gitlab-ci/)).

Another use case, which was the one I ran into when developing [git-repo], is working
with several repository services at once. You've got gitlab, github, bitbucket, gogs…
And when you're working with all of them you got to create a remote for each, and
push your changesets to each of them everytime:

``` bash
git remote add github https://github.com/guyzmo/git-repo
git remote add gitlab https://gitlab.com/guyzmo/git-repo
git remote add bitbucket https://bitbucket.org/guyzmo/git-repo
git remote add home https://gitlab.myserver.com/guyzmo/git-repo
git remote add gogs https://gogs.myserver.com/guyzmo/git-repo
```

it's a bit boring and redundant to do so, but at least that's a task you do only
once (and you can do it faster with [a great editor](http://vim.org) on the `.git/config` file).

But each time you want to push to your projects, you got to push to each of them:

``` bash
git push github master
git push gitlab master
git push bitbucket master
git push home master
git push gogs master
```

And as you're as lazy as anybody, you'll end up only pushing to one, maybe two
of the remotes, usually `github` and `home`…

# The multiple URL remote comes to help

…But you don't really have to! You can work with multiple remotes nicely, by creating
a new remote that contains all the other remotes URLs:

``` bash
git remote add all https://github.com/guyzmo/git-repo
git remote add all set-url --add https://gitlab.com/guyzmo/git-repo
git remote add all set-url --add https://bitbucket.org/guyzmo/git-repo
git remote add all set-url --add https://gitlab.myserver.com/guyzmo/git-repo
git remote add all set-url --add https://gogs.myserver.com/guyzmo/git-repo
```

then, when it's time to push your code, you just need to run:

``` bash
git push all master
```

The only drawback is that it makes little sense to pull from a remote with multiple URL,
and when looking at your index, you'll see that the `all/master` ref is updated, but
not the other refs (`github/master`, `gitlab/master`…). So if you want to keep all the
remotes updated you've got to run:

``` bash
git fetch --all
```

which will sync back all the refs that have been updated when you pushed through the all
remote. So instead of 4/5 or more commands to repeat, you end up with only two commands.

And you can make it simpler using an alias such as:

``` bash
git config alias.pushall "!pushall() { git push all $* && git fetch --all ; }; pushall"
```

# And how is it being used in [git-repo]?

When I worked on [git-repo], I figured that's a great feature to take advantage of. So
I've implemented a customized version of the `git remote add`, that's being used under
the hood by `git <target> create`, `git <target> clone`, git <target> fork`…

This is the `git <target> add` command, and it works as follows:

``` bash
git hub add <user>/<repo> [<name>] [--tracking=<branch>] [-a]
```

there you can add to the list of remotes the repository as identified by the repo slug
(`<user>/<repo>`, a full URL to the repo works as well, as long as it matches the targetted
service provider). Then you can give a custom name to the repo and specify the branch you
want to track (with `--tracking`). The `-a/--alone` parameter is to prevent from adding
the URL to the `all` remote.

``` bash
% git hub add foobar/project foobar --tracking=devel
Successfully added `foobar/project` as remote named `foobar`
% git remote
all
foobar
github
% git remote get-url --all all
git@github.com:guyzmo/clait
git@github.com:foobar/project
```

As a nice to have idea I'd like to implement would be to make the `add` command so it is possible
to handle `remote add` with just any repository, something that's like:

``` bash
% git <target> add user@10.0.0.1:./repository.git local_machine --tracking=devel
Successfully added `user@10.0.0.1:./repository.git` as remote named `local_machine`
```

At the time of writing this article, the feature [has been implemented](https://github.com/guyzmo/git-repo/compare/devel...features/repo_add_cmd?expand=1),
and will be merged to one of the future versions of [git-repo].

[git-repo]:https://github.com/guyzmo/git-repo
