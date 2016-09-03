---
type: post
categories: hack
tags: [ hack, python, storage, peer-to-peer ]
title: "Proof of Concept : Document Oriented Distributed Storage System"
date: 2010-11-17T13:21:03+02:00
summary: "I just released my Master's work done during my Internship at Bearstech. The code has been released under GPLv3 on my github. The goal of that project is to build some kind of distributed middleware that stores and share data across different nodes (whatever they are) indexed by metadata. For instructions on installing and using it, please read the wiki page."
lang: english
aliases:
 - /hack/on/proof-of-concept-:-document-oriented-distributed-storage-system/
---
I just released my Master's work done during my Internship at
[Bearstech](http://bearstech.com). The code has been released under GPLv3 on :

 * [http://forge.bearstech.com/trac/wiki/DDBFS](http://forge.bearstech.com/trac/wiki/DDBFS)

The goal of that project is to build some kind of distributed middleware that 
stores and share data across different nodes (whatever they are) indexed by 
metadata. 

As the internship, and thus the length of that project was only 5 months, I had
to make severe technological choices that made that code only a proof of concept,
instead of really usable user-end code.

So the main goals of the project are :

 * to build a modular middleware that can work as client-server (though the idea is to build it peer-to-peer ultimately) 
    * the client being a proxy for the user interfaces and 
    * the server being one entry point to the system,
 * a module to store files in a storage cluster, I used Tahoe-LAFS for this purpose because of the simplicity of its design and its features
 * a database module to store metadata, for which I used SQLite for the simplicity of its implementation, though it misses distributed features.
 * provide different UIs to show the spectrum of usage such a project can provide
    * a GUI interface with a ''Miller Columns''-like ergonomy
    * a CLI interface, useful for testing and for nerds that provides a svn-like ergonomy
    * a FUSE implementation, to show that one can build an arborescent view of such a system to keep compatibility with our operating systems

Further UI implementations, in order to make the PoC complete, should have been
an integration to indexing tools such as Beagle/trackd/spotlight, or even
nautilus and gnome. But because of the short duration I had for the development
of the project, I preferred to let that apart and focus on making it simple
and working.

![DDBFS GUI](/img/DDBFS_gui.jpeg "DDBFS GUI, Nov 2010")

If someone wants to reuse my code, don't hesitate to contact me, I'll put a copy on github though the main repository will remain at [bearstech's forge](svn://svn.bearstech.com/forge/DDBFS/). For instructions read [the wiki page](http://forge.bearstech.com/trac/wiki/DDBFS).

Finally I'd like to really thank the [Tahoe-LAFS community](http://tahoe-lafs.org) for
being friendly and helpful, with a special note for [Zooko](http://pubgrid.tahoe-lafs.org/uri/URI:DIR2-RO:ixqhc4kdbjxc7o65xjnveoewym:5x6lwoxghrd5rxhwunzavft2qygfkt27oj3fbxlq4c6p45z5uneq/blog.html)
as well as [Matthias Grawinkel](http://matthias.grawinkel.com/) for his many insights.
