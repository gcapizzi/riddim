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


from requests.exceptions import RequestException

from bs4 import BeautifulSoup


class RequestsHttpClient:

    def __init__(self, session):
        self.session = session

    def get(self, url, params):
        try:
            return self.session.get(url, params).text()
        except RequestException:
            return False


class RiddimguideBeautifulSoupParser:

    def __init__(self, soup):
        self.soup = soup

    def tunes(self):
        rows = self.soup.select('.results tr')

        tunes = []
        for row in rows[1:]:
            columns = row.find_all('td')
            tunes.append({'artist':   columns[0].get_text().strip(),
                          'song':     columns[1].get_text().strip(),
                          'riddim':   columns[2].get_text().strip(),
                          'year':     columns[3].get_text().strip(),
                          'label':    columns[4].get_text().strip(),
                          'producer': columns[5].get_text().strip()})

        return tunes

    def next(self):
        links = self.soup.select('.tunes_navigation a[rel=next]')

        if (links):
            return links[0]['href']
        else:
            return False


class RiddimguideSearchEngine:

    def __init__(self, parser_factory, http_client=RequestsHttpClient):
        self.parser_factory = parser_factory
        self.http_client = http_client

    def _query_url(self, query):
        return 'http://www.riddimguide.com/tunes?q=' + query

    def search(self, query):
        results = []
        current_query = self._query_url(query)

        while True:
            html_results = self.http_client.get(current_query)
            parser = self.parser_factory.from_html(html_results)
            results.extend(parser.tunes())

            next = parser.next()
            if next:
                current_query = next
            else:
                break

        return results

