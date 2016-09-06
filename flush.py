#!/usr/bin/env python
# -+- encoding: utf-8

from __future__ import print_function, unicode_literals
import sys

try:
    import requests
except ImportError:
    print('Missing requirement: module requests')
    sys.exit(1)
try:
    import pendulum
except ImportError:
    print('Missing requirement: module pendulum')
    sys.exit(1)
from datetime import timedelta as td

from lxml import etree

def flush():
    with open(sys.argv[1], 'r') as f:
        doc = etree.parse(f)

        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        res = None

        for elt in doc.xpath('//sm:url', namespaces=ns):
            loc = elt[0].text
            if len(elt) == 2:
                lastmod = pendulum.parse(elt[1].text)
            else:
                lastmod = pendulum.parse('1984')

            if pendulum.now()-lastmod < td(hours=1):
                print("Purge from varnish {}: ".format(loc), end='')
                res = requests.request("PURGE", loc)
                if res.status_code == 200:
                    print("Success 👍")
                else:
                    print("Failure 👎")

        if not res:
            print("No new updates detected, cache not purged.")

if __name__ == "__main__":
    flush()

