#!/usr/bin/env python
# encoding: utf-8
#
# Riddim - find info about reggae tunes!
# Copyright (c) 2013 Giuseppe Capizzi
# mailto: g.capizzi@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest

from nose.tools import *
from exam.mock import Mock, call

from requests import Session
from bs4 import BeautifulSoup

from riddim import RiddimguideBeautifulSoupParser, RiddimguideBeautifulSoupParserFactory, RequestsHttpClient, RiddimguideSearchEngine


class RiddimguideBeautifulSoupParserIntegrationTest(unittest.TestCase):

    def test_parse(self):
        soup = BeautifulSoup(open('tests/test.html').read())
        parser = RiddimguideBeautifulSoupParser(soup)
        tunes = parser.tunes()

        self.assertEquals(7, len(tunes))

        tune = {'artist': 'Bob Marley & Wailers',
                'song': 'Exodus',
                'riddim': 'Exodus',
                'year': '1977',
                'label': 'Tuff Gong',
                'producer': 'Robert Nesta \'Bob\' Marley & The Wailers'}

        self.assertEquals(tune, tunes[1])

    def test_next(self):
        soup = BeautifulSoup(open('tests/test.html').read())
        parser = RiddimguideBeautifulSoupParser(soup)

        self.assertFalse(parser.next())

        soup_nav = BeautifulSoup(open('tests/test_nav.html').read())
        parser_nav = RiddimguideBeautifulSoupParser(soup_nav)

        self.assertEquals("/tunes?q=one%20love&c=&page=2", parser_nav.next())


class RiddimguideSearchEngineIntegrationTest(unittest.TestCase):

    def test_search(self):
        parser_factory = RiddimguideBeautifulSoupParserFactory()
        http_client = RequestsHttpClient(Session())
        engine = RiddimguideSearchEngine(parser_factory, http_client)

        tunes = engine.search('bob marley')

