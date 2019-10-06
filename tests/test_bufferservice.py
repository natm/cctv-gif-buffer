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

    def test_init_one_camera_with_mqtt_auth(self):
        mockconfig = {
            "cameras": {
                "ch1": {
                    "name": "ch1",
                    "url": "rtsp://admin:admin@192.168.0.9:554/Streaming/Channels/102"
                }
            },
            "mqtt": {
                "host": "mqtt.home.local",
                "port": 1883,
                "user": "buffer",
                "pass": "buffer123",
                "topic": "buffer/prod"
            }
        }
        bs = BufferService(config=mockconfig)
        self.assertIsNotNone(bs)

    def test_init_one_camera_with_mqtt_noauth(self):
        mockconfig = {
            "cameras": {
                "ch1": {
                    "name": "ch1",
                    "url": "rtsp://admin:admin@192.168.0.9:554/Streaming/Channels/102"
                }
            },
            "mqtt": {
                "host": "mqtt.home.local",
                "port": 1883,
                "topic": "buffer/prod"
            }
        }
        bs = BufferService(config=mockconfig)
        self.assertIsNotNone(bs)