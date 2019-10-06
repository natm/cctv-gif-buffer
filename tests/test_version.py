#!/usr/bin/env python
# Nat Morris (c) 2017, 2019

import cctvbuffer
import unittest


class TestVersion(unittest.TestCase):

    def test_version(self):
        ver = cctvbuffer.version()
        self.assertIsNotNone(ver)
