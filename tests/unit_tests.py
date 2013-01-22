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

from requests.exceptions import RequestException

from riddim import RequestsHttpClient, RiddimguideSearchEngine


class RequestsHttpClientTest(unittest.TestCase):

    def test_get_ok(self):
        session = Mock()
        resp = Mock()
        resp.text.return_value = 'some text'
        session.get.return_value = resp
        http_client = RequestsHttpClient(session)

        response = http_client.get('an url', {'some': 'params'})

        session.get.assert_called_with('an url', {'some': 'params'})
        resp.text.assert_called_with()
        self.assertEquals('some text', response)

    def test_get_fail(self):
        session = Mock()
        session.get = Mock(side_effect=RequestException)
        http_client = RequestsHttpClient(session)

        response = http_client.get('an url', {'some': 'params'})

        session.get.assert_called_with('an url', {'some': 'params'})
        self.assertEquals(False, response)


class RiddimguideSearchEngineTest(unittest.TestCase):

    def test_search(self):
        parser_1 = Mock()
        parser_1.next.return_value = 'next_url'
        parser_1.tunes.return_value = [{'one': 1}, {'two': 2}]

        parser_2 = Mock()
        parser_2.next.return_value = False
        parser_2.tunes.return_value = [{'three': 3}, {'four': 4}]

        parser_factory = Mock()
        parser_factory_returns = [parser_1, parser_2]
        def parser_factory_mock(*args):
            return parser_factory_returns.pop(0)
        parser_factory.from_html = Mock(side_effect=parser_factory_mock)

        http_client = Mock()
        http_client_returns = ['page 1', 'page 2']
        def http_client_mock(*args):
            return http_client_returns.pop(0)
        http_client.get = Mock(side_effect=http_client_mock)

        engine = RiddimguideSearchEngine(parser_factory, http_client)

        tunes = engine.search('query')

        expected_calls = [call('http://www.riddimguide.com/tunes?q=query'),
                          call('next_url')]
        self.assertEquals(expected_calls, http_client.get.call_args_list)

        expected_calls = [call('page 1'), call('page 2')]
        self.assertEquals(expected_calls, parser_factory.from_html.call_args_list)

        expected_tunes = [{'one': 1}, {'two': 2}, {'three': 3}, {'four': 4}]
        self.assertEquals(expected_tunes, tunes)

