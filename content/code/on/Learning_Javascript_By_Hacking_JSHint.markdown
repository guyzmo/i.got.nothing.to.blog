---
type: post
categories: code
tags: [ javascript, jshint, lint, project, code ]
title: "Learning Javascript by hacking JSHint"
date: 2013-03-18T13:27:44+02:00
summary: "About ten days ago, I decided I should learn Javascript. I used to have a terrible opinion about that language, mostly because all I knew about it was the very bad parts… So I decided to give it a try and work on the JSHint lint to add new language features."
lang: english
logo: /img/jshint.png
header_background: /img/jshint.png
aliases:
 - /hack/on/learning-javascript-by-hacking-jshint/
---

About ten days ago, I decided I should learn Javascript. I used to have a terrible opinion
about that language, mostly because all I knew about it was the very bad parts… All globals,
weak typing years of irritating approach for web programing.

Go for javascript
=================

But then, at FOSDEM 2013, I let me convinced by my Mozillian friends that it is actually not
such a bad language, and it is possible to make clean and neat code while ignoring those bad
parts. Then I thought that even the holy C has its share of bad stuff, so why not give it a 
try?

So, I decided to buy and read Crockford's book about the "Good parts" of Javascript (pretty
appealing, when we only know about the bad ones), and updated my knowledge of [the bad stuff](http://www.wooji-juice.com/blog/javascript-article.html).
And that let me discover more deeply hidden [bad stuff](http://johnkpaul.github.com/presentations/empirejs/javascript-bad-parts/#/3).

But there's hope, and that's for the next real version of Javascript, being currently drafted
by the Javascript committee. That's how I discovered the specification of the let keyword that
introduces real block scoping to Javascript, destructuring expressions and a few other features
that I would have missed having spent a few years in the Python world.

I also went over the Javascript pages of mozilla and discover they implemented a lot of really
neat little features before they were considered or being considered stable in the draft.

Getting dirty: working on the JSHint linter
===========================================

While I was testing scripts and language features, I could get easily lost by all
the different ways to write a code and how a simple typo can make a code break in
weird ways. That's why I installed [syntastic](https://github.com/scrooloose/syntastic) plugin
for vim that uses [jshint](http://jshint.com) as backend lint for Javascript.

But whenever I was using a new or non-standard syntax, the lint would consider my code
as buggy and that was really unpleasant, as I was still learning and couldn't tell whether
the lint or my code is wrong. That's how I considered getting into the source of [JSHint](https://github.com/jshint/jshint)
and update its features.

I have already worked on three compilers in my life, and thought that the algorithmic 
principle would remain the same, so the language's features and syntactic sugar would
become more obvious to me.

JSHint is based on JSLint, written by Douglas Crockford himself (and for the anecdote,
when I looked at a git blame on the parser source, only blank lines were still from
his code ;-) ). Basically it implements a [Pratt Parser](http://en.wikipedia.org/wiki/Pratt_parser),
using the principle of top-down operator precedence, associating semantic rules with the
first token on the line, instead of using a grammar rule.

On the good side, it makes the code really easy to understand, as most of the time to
understand how a language feature is implemented, you shall begin with the first token,
and read the code to get where you need. On the other side, it makes semantic rules harder
to implement and look like a dirty hack when there's ambiguity on the first token.

Two problematic cases were the ambiguity between destructuring expressions, array 
comprehension and JSON syntax, and the second one was all the let syntaxes implemented
by mozilla. The solution is always to look ahead what kind of tokens will be used (which
mimics the purpose of a grammar based set of rules), to decide what kind of construct is
being used.

What did I learn?
=================

Javascript is a really easy language, though not really simple, and has some functional
programing features that can make it almost as elegant as a real functional language. I
could cite many of the chapters from the Crockford's book, "recursion", "Scope", 
"Closure", "Callbacks", "Cascade", "Curry", "Memoization"… I've met most of those features
and patterns in the parser, that made it a really cool real world exercise.

Real world use of good practices
--------------------------------

The heart of the JSHint parser is the `expression()` function. It will decide what can of
expression it is (as formalized by the Pratt Parser algorithm) and call functions associated
with the first token's identity.

Then, every token will get an associated function by the use of handlers functions (like `prefix`,
`infix` or `stmt`) that takes a token's name as first argument, and the applied function as second
argument. That "handler" function will bind the actual parsing function to the given token type, 
using the Pratt Parser formalism. That's a cool example of the use of a mix of the language 
features exposed by Crockford.

New features
------------

But I've also got deeply into the new syntaxes ES6 will offer, or Mozilla implemented for
their javascript engine. 

* let token: block scoping… and more

I have implemented the new blockscoping feature, with the `let` token that declares a
variable in that scope. That feature is pretty neat, as it can help use variables more 
closely to were they are being used.

But what is even better, imho, is the mozilla extensions to the `let` keyword, that defines
a new let expression, so you can declare and define a bound variable local to an expression:

   var y=2;
   let(x=1) print(x, y);
   print(let(x=1) x, y);

* destructuring expressions

That's something that should be in every high level language. It helps declare a bunch of
variables out of an array or an object. It becomes really important in Javascript for the
`require` mechanism, so you can easily select what you want to import. New Mozilla APIs are
using it a lot:

   const {foo, bar} = require("foobar");

instead of

   var foobar = require("foobar");
   var foo = foobar.foo;
   var bar = foobar.bar;

* array comprehensions

That's also some syntactic sugar that is really helpful by times, but can make a code
really hard to read some other times. The first implementation of such a feature is in
current Mozilla's JS implementations, though the EcmaScripct committee is deprecating
it in its current version. The first implementation is harder to implement in a parser
and unnatural to read (you use first what you will define after), but is very similar
to the python syntax.

   let foo = [x for (x of [1, 2, 3, 4, 5, 6]) if (x % 2 === 0)]

Whereas [the new drafted syntax](https://github.com/rwldrn/tc39-notes/blob/master/es6/2013-01/jan-31.md#comprehensionsgenerator-syntax) is simpler to implement and read
but will be confusing for people from the python world:

   let foo = [for (x of [1, 2, 3, 4, 5, 6]) if (x % 2 === 0) x]

the latter syntax is still not implemented in JSHint as of today, but it will be as
soon as the esnext/moz syntax features are correctly decorralated.

* function generators

The introduction of the `yield` keyword to create generators so one can iterate
over the results of a function while the function is iterating is really a great
new feature. The only perk, is that the ES6 committee introduced the `function*`
token to identify generator functions, whereas Mozilla already implemented it using
the standard `function` token. Both syntaxes will be supported in either the `esnext`
or `moz` mode.

* Mozilla specific features

And finally, I implemented a few really neat mozilla specific language features, such
as mutiple catch block support, as well as conditional expressions in catch. Function
expression closure, `for each` support (that is now deprecated towards `for of`)…
Most of them being explained over [here](http://ejohn.org/blog/javascript-18-progress/) or [on MDN](https://developer.mozilla.org/en-US/docs/JavaScript/New_in_JavaScrip).

To conclude
-----------

I have discovered a new language and the approach that goes with it. Sadly the web is
full of bad answers for bad questions about javascript, but that's because it is a language
being used by a lot of people. Java has still the same problem (and that's maybe their second
common point after their name :-) ).

I'm a bit sad to discover that the language evolution is still being teared between implementors
and comittees that can't get something as standard as it would be needed for the Great Interoperability
of the Web. But I hope that the comitte will make things right, and that we won't have to wait 2018
to have JS as correct as it would be needed *today*.

I still got some trouble apprehending the different contexts of the variable `this` in function
calls, and I think it is one of the worst things about Javascript. I like behaviours to be homogeneous
and simple, and `this` is not the case. But I have hope that the `=>` syntax that is being considered
stable in most recent drafts will improve the situation, by not setting `this` up anymore, but doing it
explicitely.

