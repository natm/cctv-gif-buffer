#!/usr/bin/env python
# Nat Morris (c) 2017, 2019
"""CCTV buffer - Buffer Service."""

import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from cctvbuffer import version
from cctvbuffer.camera import Camera
from cctvbuffer.mqttconnector import MqttConnector
from cctvbuffer.web.server import WebServer

LOG = logging.getLogger(__name__)


class BufferService(object):

    def __init__(self, config):
        LOG.info("BufferService v%s initializing", version())
        self.config = config
        self.cameras = []
        self.tokens = []
        self.mqtt = MqttConnector(bufferservice=self)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.mqtt.job_publish_status)
        self.scheduler.add_job(func=self.mqtt.job_publish_status, trigger=CronTrigger.from_crontab("* * * * *"))
        self.scheduler.add_job(func=self.mqtt.job_publish_cameras)
        self.scheduler.add_job(func=self.mqtt.job_publish_cameras, trigger=CronTrigger.from_crontab("* * * * *"))
        self.startup = time.time()
        self.webserver = WebServer(bufferservice=self)

    def start(self):

        # load cameras
        for camid in self.config["cameras"]:
            camcfg = self.config["cameras"][camid]
            self.cameras.append(Camera(id=camid, url=camcfg["url"], name=camcfg["name"]))

        LOG.info("Starting MQTT")
        self.mqtt.start()

        LOG.info("Starting scheduler")
        self.scheduler.start()

        LOG.info("Starting webserver")
        self.webserver.start()

        LOG.info("Starting %d cameras", len(self.cameras))
        for camera in self.cameras:
            camera.start()

        LOG.info("Entering main thread loop")
        while True:
            time.sleep(5)

    @property
    def uptime(self):
        return int((time.time()-self.startup)/60)
