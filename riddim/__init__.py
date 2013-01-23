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


import re
from urlparse import urljoin

from requests.exceptions import RequestException

from bs4 import BeautifulSoup


class RequestsHttpClient:

    def __init__(self, session):
        self.session = session

    def get(self, url, params = {}):
        try:
            return self.session.get(url, params=params).text
        except RequestException:
            return False


class RiddimguideBeautifulSoupParser:

    def __init__(self, soup):
        self.soup = soup

    def _remove_escapes(self, text):
        regex = re.compile('(\n|\t)')
        return regex.sub('', text)

    def _text(self, element):
        text = element.get_text().strip()
        return self._remove_escapes(text)

    def _tune_from_columns(self, columns):
        return {'artist':   self._text(columns[0]),
                'song':     self._text(columns[1]),
                'riddim':   self._text(columns[2]),
                'year':     self._text(columns[3]),
                'label':    self._text(columns[4]),
                'producer': self._text(columns[5])}

    def _tune_from_row(self, row):
        columns = row.find_all('td')
        return self._tune_from_columns(columns)

    def tunes(self):
        rows = self.soup.select('.results tr')
        return [self._tune_from_row(row) for row in rows[1:]]

    def next(self):
        links = self.soup.select('.tunes_navigation a[rel=next]')

        if (links):
            return links[0]['href']
        else:
            return False


class RiddimguideBeautifulSoupParserFactory:

    def from_html(self, html):
        soup = BeautifulSoup(unicode(html))
        return RiddimguideBeautifulSoupParser(soup)


class RiddimguideSearchEngine:

    BASE_URL = 'http://www.riddimguide.com'

    def __init__(self, parser_factory, http_client):
        self.parser_factory = parser_factory
        self.http_client = http_client

    def _url(self, path):
        return urljoin(self.BASE_URL, path)

    def _query_url(self, query):
        return self._url('/tunes?q=' + query)

    def search(self, query):
        results = []
        current_query = self._query_url(query)

        while True:
            html_results = self.http_client.get(current_query)

            if not html_results:
                break

            parser = self.parser_factory.from_html(html_results)
            results.extend(parser.tunes())
            next = parser.next()

            if not next:
                break

            current_query = self._url(next)

        return results
