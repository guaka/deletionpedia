# -*- coding: utf-8  -*-
import family, config

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'deleted'
        langlist = [ 'en', 'fr', 'fi', 'nl', 'de', 'es', 'it', 'pt', 'sv' ]
        self.langs = { x: x for x in langlist }

    def hostname(self, code):
        return 'deletionpedia.org'

    def scriptpath(self, code):
        if code == 'en':
            return '/w'
        else:
            return '/' + code + 'w'

        
