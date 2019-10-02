#!/usr/bin/env python
# Nat Morris (c) 2017, 2019
"""CCTV buffer - Service."""

#import collections
#import imageio
import logging
#import requests
#import threading
import json
import time
import paho.mqtt.client as mqttc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from cctvbuffer import version
from cctvbuffer.camera import Camera
from cctvbuffer.web.server import WebServer
#import io

LOG = logging.getLogger(__name__)


class BufferService(object):

    def __init__(self, config):
        self.config = config
        self.cameras = []
        self.tokens = []
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(func=self.job_publish_status)
        self.scheduler.add_job(func=self.job_publish_status, trigger=CronTrigger.from_crontab("* * * * *"))
        self.scheduler.add_job(func=self.job_publish_cameras)
        self.scheduler.add_job(func=self.job_publish_cameras, trigger=CronTrigger.from_crontab("* * * * *"))
        self.startup = time.time()
        self.webserver = WebServer(bufferservice=self)

    def start(self):

        # load cameras
        for camid in self.config["cameras"]:
            camcfg = self.config["cameras"][camid]
            self.cameras.append(Camera(id=camid, url=camcfg["url"], name=camcfg["name"]))
        LOG.info("Loaded %d cameras", len(self.cameras))

        LOG.info("MQTT setting up")
        self.mqtt = mqttc.Client()
        self.mqtt.on_connect = self.mqtt_on_connect
        self.mqtt.on_message = self.mqtt_on_message
        self.mqtt.on_subscribe = self.mqtt_on_subscribe
        self.mqtt.username_pw_set(self.config["mqtt"]["user"], self.config["mqtt"]["pass"])
        LOG.info("MQTT connecting")
        self.mqtt.connect(self.config["mqtt"]["host"], self.config["mqtt"]["port"], 60)

        # subscribe to interesting MQTT topics
        self.mqtt_topic = self.config["mqtt"]["topic"]
        for topic_suffix in ["/snapshot/request/+/now", "/animation/request/+/now"]:
            self.mqtt.subscribe(f"{self.mqtt_topic}{topic_suffix}")

        self.mqtt.loop_start()

        LOG.info("Starting scheduler")
        self.scheduler.start()

        LOG.info("Starting webserver")
        self.webserver.start()

        for camera in self.cameras:
            camera.start()

        while True:
            time.sleep(5)

    @property
    def uptime(self):
        return int((time.time()-self.startup)/60)

    def mqtt_on_connect(self, client, data, flags, rc):
        LOG.info("MQTT Connected %s", rc)

    def mqtt_on_subscribe(self, client, userdata, mid, gqos):
        LOG.info("MQTT Subscribed %s", mid)

    def mqtt_on_message(self, client, userdata, msg):
        LOG.info("MQTT Message %s %s", msg.topic, msg.payload)

    def mqtt_publish_message(self, suffix, payload, qos=0):
        topic = "%s/%s" % (self.config["mqtt"]["topic"], suffix)
        self.mqtt.publish(topic=topic, payload=payload, qos=0)

    def job_publish_cameras(self):
        # list of cameras
        summary = {}
        # per camera
        for camera in self.cameras:
            summary[camera.id] = camera.name
            try:
                self.mqtt_publish_message(suffix=f"camera/{camera.id}", payload=json.dumps(camera.state_summary()))
            except Exception as e:
                LOG.warning(e)
        self.mqtt_publish_message(suffix="cameras", payload=json.dumps(summary))

    def job_publish_status(self):
        status = {"cameras": len(self.cameras), "version": version(), "uptime": self.uptime}
        self.mqtt_publish_message(suffix="status", payload=json.dumps(status))
