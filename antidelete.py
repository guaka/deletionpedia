#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2013-2020 various people
#
# http://deletionpedia.org/
#
# Script to rescue articles from Wikipedia
# Multilingual, additions for other languages welcome
#
# Available under the terms of the GNU General Public License v2 or later
# 

import pywikibot
from pywikibot import pagegenerators
site = pywikibot.Site('en', 'wikipedia')
cat = pywikibot.Category(site,'Category:Articles for deletion')
gen = pagegenerators.CategorizedPageGenerator(cat)
for page in gen:
    site = pywikibot.Site('en', 'wikipedia')
    text = page.text
    site = pywikibot.Site('deleted', 'wikiyt')
    p = pywikibot.Page(site, page)
    p.text = text
    p.save('Inclusion power')
