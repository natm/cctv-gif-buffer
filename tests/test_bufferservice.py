#!/usr/bin/env python
# Nat Morris (c) 2017, 2019

from cctvbuffer.service import BufferService
import unittest


class TestBufferService(unittest.TestCase):

    def test_init(self):
        bs = BufferService()
        self.assertIsNotNone(bs)
