#!/usr/bin/env python
# encoding: utf-8
#
# FreiTAG - A simple song command line tool to tag and rename songs.
# Copyright (c) 2010-2011 Giuseppe Capizzi
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

from subprocess import Popen, PIPE

from nose.tools import *


class AcceptanceTest(unittest.TestCase):

    def run_riddim(self, *params):
        cmd = ['riddim'] + list(params)
        return Popen(cmd, stdout=PIPE).communicate()[0]

    def test_search_with_one_result(self):
        output = self.run_riddim('bob marley exodus', '--format={riddim}')
        self.assertEquals('Exodus\n', output)

    def test_search_with_paging(self):
        output = self.run_riddim('bob marley')
        self.assertEquals(100, len(output.splitlines()))


if __name__ == '__main__':
    unittest.main()
