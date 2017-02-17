#!/usr/bin/env python
# Nat Morris (c) 2017

import cctvgifbuffer
import unittest

class TestVersion(unittest.TestCase):

    def test_version(self):
        ver = cctvgifbuffer.version()
        self.assertIsNotNone(ver)
