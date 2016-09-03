---
type: post
categories: hack
tags: [ mail, python, mutt, notmuch, vim ]
title: "Notmuch: How I learned to stop worrying and love the mail"
date: 2013-03-20T15:43:09+02:00
summary: "After years of troubles managing my mail using several different programs, I've begun to hate MUAs because they were inconvenient and slow. But that was before I knew about notmuch."
lang: english
logo: "/img/strangelove.jpeg"
header_background: /img/drstrangelove.jpeg
aliases:
 - /hack/on/notmuch:-how-i-learned-to-stop-worrying-and-love-the-mail/ 
---

I'm a long term mutt user, I think my first mutt install was in 2000 or 2001, and by
that time I was happy with that, managing my mail in mbox. But then, I started to subscribe
to many high traffic mailing lists, and I had to create several mboxes and use mail delivery
program that can filter the mail (basically procmail). And then the mbox technology got 
overwhelmed by the quantity of mails I had, so I made a Maildir structure with many 
mailboxes within and I got even more mails to manage. Mutt got really slow, so I added 
the caching feature, and installed mairix to help speed it up. But that was still awful
to use.

Then I started to hate the mail.
================================

At that time, I tried several MUA alternatives to mutt, like Evolution, Thunderbird or
even Mail.app (yes, the closed source Apple™'s one). But they were slow, buggy, hard to
configure and anti-ergonomic… At least for a nerd like me. I still don't understand why
mutt is one of the only mail program to be able to sort mail with most recent at bottom,
which looks more logical to me, respecting the chronological queue of mails!

Let there be light.
===================

But after all those years with inconvenient and awful mail user agents, I finally discovered
`sup` by William Morgan. And that was a real revolution for me. Finally a mail program that
can handle thousand mails while being fast and convenient. Sadly that program was far from
being perfect, and in the way to reimplement it, it looks like William Morgan stopped its 
development. But that's how I discovered `notmuch`, and how I stopped worrying about the mail.


For a lot of mails, there's notmuch (to worry about)!
=====================================================

Notmuch is a standalone mail indexing program that interoperates well with the system
it lives in. It is simple, and thus follows the KISS unix principle. It goes over your
Maildir, indexes all your mail and gives you the ability to search over them. That's 
about all, and all we ask for it to do.

I installed it using the sources:

    git clone git://notmuchmail.org/git/notmuch
    cd notmuch
    ./configure --without-emacs && make && sudo make install

Then I installed the mutt-kz fork of mutt, that integrates a few patches: the old sidebar
patch (though I find it a bit more stable than it used to be), and integrates the notmuch
searches as "virtual folders" using the `notmuch://QUERY` syntax. It also adds a bunch
of new settings and commands (that can be mapped) for a better integration in mutt, and a
whole new experience.

    git clone https://github.com/karelzak/mutt-kz.git
    cd mutt-kz
    ./configure && make && sudo make install

I'll make a post about my mail configuration pretty soon.

A few improvements I wrote for my mail workflow
===============================================

But on my mail workflow, I was still missing one feature, it is the use of an addressbook.
Most of the time, it is not really problematic, I can use my brain or simply reply 
to existing threads, but sometime I can make a stupid typo that makes the mail go to /dev/null.

So I've tried a few options, but none were working the way I expected, so I decided to write
my own notmuch based addressbook program

     https://github.com/guyzmo/notmuch-abook

It integrates a vim plugin and a standalone software. The later one integrates with the
notmuch configuration file, and basically creates a sqlite3 database of all your addresses
parsed from your notmuch index, or scanning incoming mails, piping the mail headers to
the update option of the program.

The netiquette is dead and burried…
===================================

Another improvement I wanted is to have mappings in vim to easily reformat a mail
reply so I can make clean and easy to read mails, without being disturbed by people
writing awful mails. 

That's why I wrote about ten years ago a vim plugin that used to do that using Perl
Text::Format, but it did not work well with UTF-8, and had a few other perks. That's
why I finally rewrote the plugin entirely in python:

     https://github.com/guyzmo/vim-yaposting

