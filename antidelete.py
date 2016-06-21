#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) Kasper Souren 2013-2015
#
# http://deletionpedia.org/
#
# Script to rescue articles from Wikipedia
# Multilingual, additions for other languages welcome
#
# Available under the terms of the GNU General Public License v2 or later
# 

import sys
import re
import datetime
from wikipedia import *
from locale import setlocale, LC_TIME

class Antidelete:
    def __init__(self, lang, patterns):
        self.lang = lang
        self.frm = Site(lang, 'wikipedia')
        self.to = Site(lang, 'deleted')
        self.patterns = patterns

    def fetch(self):
        # There are various patterns
        print self.lang, self.patterns
        
        if 'fn_day' in self.patterns:
            self.fetch_days()
        else:
            self.parse_list(self.patterns['title'])

    def fetch_days(self):
        for i in range(7):
            self.fetch_day(i)

    def fetch_day(self, days_ago = 1):
        '''Fetch articles on the list of a specific day'''
        day = datetime.date.today() - datetime.timedelta(days_ago)
        if 'locale' in self.patterns:
            setlocale(LC_TIME, 'de_DE') #self.patterns['locale'])
        else:
            setlocale(LC_TIME, 'en_US.utf8')
        pagename = self.patterns['fn_day'](day)
        fn_title = 'fn_title' in self.patterns and self.patterns['fn_title'] or None
        self.parse_list(pagename, title_process = fn_title)

    def parse_list(self, pagename, title_process = None):
        '''Parse page with list of articles to be deleted'''
        p = Page(self.frm, pagename) 
        s = p.get()
        re_article = re.compile(self.patterns['regexp'])
        for l in s.splitlines():
            m = re_article.match(l)
            if m:
                title = m.group(1)
                if title_process:
                    # if title != 'Info': #Swedish...
                        title = title_process(title)
                self.recover_article(title)
        


    def recover_article(self, title):
        print "Recovering: " + title[:100]
        if 'Talk' in title:
            print 'no talk pages yet'
            return
        page = Page(self.frm, title)
        try:
            article_text = page.get()
        except IsRedirectPage:
            print 'IsRedirectPage?', title
            return
        except NoPage:
            print 'PROBABLY deleted already...', title
            return

        if not 'porn' in article_text and not 'xxx' in article_text:
            dp_page = Page(self.to, title)

            update_page = False
            try:
                if dp_page.get() != article_text:
                    update_page = True
                else:
                    print 'PAGE already rescued'
            except pywikibot.exceptions.NoPage:
                update_page = True
            if update_page:
                if self.patterns['test'] in article_text:
                    msg = 'inclusion power'
                else:
                    article_text = "{{survived}}"
                    msg = 'survived on Wikipedia'
                dp_page.put(article_text, msg)


if __name__ == '__main__':

    patterns = {}
    patterns['sv'] = {
        'title': u'Wikipedia:Sidor_föreslagna_för_radering',
        'regexp': u'{{Wikipedia:Sidor föreslagna för radering/(.*)}}',
        'test': '{{sffr}}', # not very talkative
        }
    patterns['de'] = {
        'fn_day': lambda d: u'Wikipedia:Löschkandidaten/' + d.strftime('%d. %B %Y'),
        'locale': 'de_DE',
        'regexp': '== \[\[(.+)\]\]',
        'test': u'{{Löschantragstext',
        }
    patterns['en'] = {
        'test': 'Article for deletion',
        'regexp': '{{Wikipedia:Articles for deletion/(.*)}}',
        'fn_day': lambda d: 'Wikipedia:Articles_for_deletion/Log/' + d.strftime('%Y_%B_%e'),
        'fn_title': lambda t: t.replace(' (2nd nomination)', ''),
        }
    patterns['fi'] = {
        'test': 'oistoäänestys}}',
        'regexp': '{{/(.*)}}',
        'title': u'Wikipedia:Poistoäänestykset'
        }
    patterns['fr'] = {
        'test': 'uppression}}',
        'regexp': '[*]{{L[|](.*)}}',
        'title': u'Wikipédia:Pages_à_supprimer'
        }
    patterns['nl'] = {
        'test': '{{wiu|',
        'regexp': '[*]\[\[(.+)\]\]',
        'fn_day': lambda d: "Wikipedia:Te beoordelen pagina's/Toegevoegd " + d.strftime('%Y%m%d')
        }
    for lang in ['de', 'en', 'fi', 'nl', 'fr', 'sv']:
        ad = Antidelete(lang, patterns[lang])
        ad.fetch()
