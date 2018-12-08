---
type: post
tags: [ web, datadog, monitoring, sysadmin, devops ]
title: "An integration story: datadog agents on clever-cloud"
date: 2018-12-08T19:50:09+02:00
summary: "Integrating datadog on a system that's not included in their deploy script is not straightforward,
          it took some time and pain of figuring things out, but in the end, it iss actually straightforward.
          Through this blog post, I figured I'd share my experience, while writing that missing piece of
          documentation, on how to build and deploy the datadog agents."
lang: english
logo: /img/data-dog.png
tweet: 1072136197651214336
header_background: /img/nasa-apollo-ops.jpeg
---

# tl;dr

integrating datadog on a system that's not included in their `curl | bash` script is not straightforward,
it took some time and pain of figuring things out, but in the end, it's actually straightforward. So I figured through this
blog post, I'd share my experience, while writing that missing piece of documentation, on how to build and deploy the datadog
agents. [Click here to skip the story, and get to the real stuff](#enough-talk-let-s-get-real)

# Why would I need that?

At my [dayjob](https://zeloce.com), I've inherited a rails project, and the legacy is far from stellar. One
of the major problems I'm having is that I'm getting regularly `ENOMEM` crashes on the workers (the task
queues). When that happen, the queue loop dies, but the process stays, making it impossible for the watchdog
to restart them.

![](/img/chihiro_no_face_glouton.jpeg)

So, I can either triple how much I'm spending in hosting to have some peace, or I can profile my service,
to see what's going on in terms of memory usage, latency all across the stack.
And then, with data, I can understand what's going on, and verify that my fixes actually work.

To that end, because I've used it on another project in the past, and because it is integrating system metrics,
process monitoring, APM and logs, I figured the best tool to that end was to use [Datadog](https://datadoghq.com).
Their dashboards are quite mature, with the ability to dig in metrics and/or correlate them makes it a great tool.
Also, their log manager based on logmatics is definitely a plus, as I was their customer before the
datadog+logmatics merge.

There definitely are other projects (FLOSS or SaaS) that are worth checking out, but from my past experience
installing and using datadog was painless, so I decided to integrate it in my project. Never figured it would
be easy to do but hard to figure…

# Hosting service

My hosting service is [Clever-Cloud](https://clever-cloud.com), they've got an awesome platform (in terms of ops
UX, as well as what they told me about their technical architecture), and the team is not only reachable but nice
considerate and willing to help!

![](/img/clever-cloud.svg)

What's very specific about them is that unlike other services their instances (which actually are real VMs, not
containers) are not based on the mainstream linux distributions, but on a Gentoo fork: [Exherbo](https://exherbo.org),
and they don't give you root over the VM. So there's no way to `apt-get install` stuff, or mutate `/etc/` files.

This is never an issue, because anyway when you deploy your code, you just need to tell the PaaS where to bind the
ports your code will be listening on, how to build your code, and how to run it. No point in hacking around elsewhere.

# The integration pain

When you open your account on Datadog, you reach the agent installation page. They offer you diverse solutions for MacOs,
Windows, Debian, Ubuntu, Redhat, Amazon, Docker… Each of them being a variant of:

    bash -c $(curl -L https://raw.githubusercontent.com/...)

And when you look at the script, it's basically doing a uname to check what system you're on, so it installs itself on
it, by installing through the package manager. No comment.

<center>
![`¯\_(ツ)_/¯`](/img/trollface_shrug.png)
</center>

Thankfully, they also provide step-by-step instructions for some platforms, to do the same, but knowingly.

But on that agent installation page, they offer no solution for clever-cloud, or for Exherbo, the catch-all solution
is given at the end of the list: *From Source*.

There, it's said:

> Source install is only available in version 5 of the Agent. Build the Agent binary for version 6 or later following the instructions in the project pages on GitHub.

But if you look further, agent v5 is not supporting all the neat features I want, I do really need v6. So I looked
at the instructions on the project pages, which tells you how to build the agent, without much context, you're basically
on your own there. I mean, fine, you can build it, but how to actually replicate what's packaged for the supported systems?

So I followed the instructions, and as it's all in go, I just compiled the agent and vendored the binary and the configuration
in my sources. Then, I just spawned it as a worker, and it actually worked 🙌. I also included the APM library in my code, and
thought that the agent would be forwarding the metrics from the library to their servers… But no luck. I tried tickering their
configuration without luck, and even had a discussion with the support, who were as clueless as I was.

It's only after a month or so that while scrolling through all the DataDog's repositories that I found out there were different
source repositories for the [Datadog-Agent](https://github.com/DataDog/datadog-agent), which I compiled, vendored
and deployed, and two other agents: the [Datadog-Trace-Agent](https://github.com/DataDog/datadog-trace-agent) and
the [Datadog-Process-Agent](https://github.com/DataDog/datadog-process-agent). There was no mention of it anywhere in
the docs… 🤷

<center>
![](https://imgs.xkcd.com/comics/tools.png)
</center>

Then I followed the READMEs, compiled each agent, and after a little tickering of the configuration, I had process and
APM reporting back to datadog 🙌. There's one thing though that makes no sense: you got three agents repositories, the
three of them are in Go, and each of them shall be built with a different toolset. Come on, datadog people… I know you
can do better ☺

Finally, the last thing I wanted to integrate was the logs. And thankfully, I had no need to hack things around, because
Clever-Cloud implements RSysLog compatible log drains, and Datadog has an endpoint to receive that (given a little configuration
that the Clever-Cloud team did for me thank you mates 👍).

# Enough talk, let's get real

<center>
![let's hack!](/img/ncis-hack.gif)
</center>

First you have to build [Datadog-Agent](https://github.com/DataDog/datadog-agent#getting-started), in a nutshell:

```
% git clone https://github.com/DataDog/datadog-agent.git $GOPATH/src/github.com/DataDog/datadog-agent
% cd $GOPATH/src/github.com/DataDog/datadog-agent
% virtualenv -p python2.7 var
% source var/bin/activate
% pip install -r requirements.txt
% invoke deps
% INVOKE_USE_SYSTEM_LIBS=false var/bin/invoke agent.build --build-exclude=snmp
% deactivate
```

That last line environment setting is important to make an *embedded* build (I guess they mean statically built)
so it can be cross-compiled and deployed on another system (I'm building on an Arch linux, while deploying in an Exherbo VM).

Finally, once it's built, you get a `bin/agent` directory that's 70MB (the agent itself weights 64MB), you can take that directory
and move within your source to vendor the agents (or build a tar package that you'll store somewhere and pull when needed).

```
# I like to keep misc stuff in the contrib dir of my projects
# so here we're copying the whole bin/agent subtree as contrib/datadog in the sources
% cp -r bin/agent $MY_PROJECT_SOURCE_ROOT/contrib/datadog
```

Then let's proceed with building the [trace agent](https://github.com/DataDog/datadog-trace-agent):

```
% go get -u github.com/DataDog/datadog-trace-agent/...
% cd $GOPATH/src/github.com/DataDog/datadog-trace-agent
% make install
% cp $GOPATH/bin/trace-agent $MY_PROJECT_SOURCE_ROOT/contrib/datadog
```

There the trace agent is also vendored within your sources.

And finally, let's build the [process agent](https://github.com/DataDog/datadog-process-agent):

```
% cd $GOPATH/src/github.com/DataDog
% git clone git@github.com:DataDog/datadog-process-agent.git
% cd datadog-process-agent
% rake deps
% rake install
% cp $GOPATH/bin/process-agent $MY_PROJECT_SOURCE_ROOT/contrib/datadog
```

And now you've got it all vendored, well, don't forget to add and commit it!

```
% cd $MY_PROJECT_SOURCE_ROOT
% git add contrib/datadog
% git ci -m 'Adds datadog agents'
```

Then you've got to configure the agents, most of it is done through one file:

```
% nvim contrib/datadog/dist/datadog.yaml
```

Here's my configuration:

```
% grep -v '^#.*$\|^$' contrib/datadog/dist/datadog.yaml
use_dogstatsd: true
bind_host: localhost
logs_enabled: true
process_config:
  enabled: "true"
apm_config:
  enabled: true
  analyzed_spans:
    # here you add the lines suggested in the apm analytics page on datadog
    # for example, to watch the ruby grape mount:
    grape|grape.endpoint_run: 1
```

I can only advice you to check out the documentation and tweak the configuration
and the `conf.d` files ([to fetch redis metrics for example](https://docs.datadoghq.com/integrations/redisdb/)).

Finally, to get the logs on datadog from clever-cloud, all I have to do [is configure a drain](https://github.com/CleverCloud/clever-tools#logs-drains):

```
% clever drain create -a $MY_CLEVER_APP_NAME -k $DATADOG_API_KEY Datadog tcp://intake.logs.datadoghq.com:10514
```

which will create an RSyslog drain with [the special datadog configuration](https://docs.datadoghq.com/integrations/rsyslog/),
so that all logs will get forwarded directly by clever-cloud to the datadog endpoint.

<center>
![Configured Datadog Dashboard screenshot](/img/datadog-dashboard.png)
</center>

And finally you're all set 🙌

<center>
![](/img/a-team.webp)
</center>

