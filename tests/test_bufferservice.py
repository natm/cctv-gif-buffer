#!/usr/bin/env python
# Nat Morris (c) 2017, 2019

from cctvbuffer.service import BufferService
import unittest


class TestBufferService(unittest.TestCase):

    def test_init_one_camera(self):
        mockconfig = {
            "cameras": {
                "ch1": {
                    "name": "ch1",
                    "url": "rtsp://admin:admin@192.168.0.9:554/Streaming/Channels/102"
                }
            }
        }
        bs = BufferService(config=mockconfig)
        self.assertIsNotNone(bs)
