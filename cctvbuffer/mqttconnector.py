#!/usr/bin/env python
# Nat Morris (c) 2017, 2019

import logging
import json
import paho.mqtt.client as mqttc
from apscheduler.triggers.cron import CronTrigger
from cctvbuffer import version

LOG = logging.getLogger(__name__)


class MqttConnector(object):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice
        self.config = self.bufferservice.config
        self.enabled = False
        if "mqtt" in self.config:
            self.enabled = True

        if self.enabled:
            self.mqtt = mqttc.Client()
            self.mqtt_config = self.config["mqtt"]
            # MQTT event hooks
            self.mqtt.on_connect = self.mqtt_on_connect
            self.mqtt.on_message = self.mqtt_on_message
            self.mqtt.on_subscribe = self.mqtt_on_subscribe
            self.mqtt_base_topic = self.mqtt_config["topic"]
            # MQTT scheduled publish jobs
            self.bufferservice.scheduler.add_job(func=self.job_publish_status)
            self.bufferservice.scheduler.add_job(func=self.job_publish_status, trigger=CronTrigger.from_crontab("* * * * *"))
            self.bufferservice.scheduler.add_job(func=self.job_publish_cameras)
            self.bufferservice.scheduler.add_job(func=self.job_publish_cameras, trigger=CronTrigger.from_crontab("* * * * *"))

    def start(self):
        if self.enabled:
            LOG.info("MQTT Starting")
            if "user" in self.mqtt_config and "pass" in self.mqtt_config:
                self.mqtt.username_pw_set(self.mqtt_config["user"], self.mqtt_config["pass"])
            LOG.info("MQTT Connecting")
            self.mqtt.connect(self.mqtt_config["host"], self.mqtt_config["port"], 60)

            # Subscribe to interesting MQTT topics
            topics = [
                "/snapshot/request/+/now",
                "/animation/request/+/now"
            ]
            for topic_suffix in topics:
                self.mqtt.subscribe(f"{self.mqtt_base_topic}{topic_suffix}")

            # Start a background thread to maintain the MQTT connection
            self.mqtt.loop_start()

    def mqtt_on_connect(self, client, data, flags, rc):
        LOG.info("MQTT Connected %s", rc)

    def mqtt_on_subscribe(self, client, userdata, mid, gqos):
        LOG.info("MQTT Subscribed %s", mid)

    def mqtt_on_message(self, client, userdata, msg):
        LOG.info("MQTT Message %s %s", msg.topic, msg.payload)

    def mqtt_publish_message(self, suffix, payload, qos=0):
        topic = "%s/%s" % (self.mqtt_base_topic, suffix)
        self.mqtt.publish(topic=topic, payload=payload, qos=0)

    def job_publish_cameras(self):
        summary = {}
        # Per camera
        for camera in self.bufferservice.cameras:
            summary[camera.id] = camera.name
            try:
                self.mqtt_publish_message(suffix=f"camera/{camera.id}", payload=json.dumps(camera.state_summary()))
            except Exception as e:
                LOG.warning(e)
        self.mqtt_publish_message(suffix="cameras", payload=json.dumps(summary))

    def job_publish_status(self):
        status = {
            "cameras": len(self.bufferservice.cameras),
            "uptime": self.bufferservice.uptime,
            "version": version()
        }
        self.mqtt_publish_message(suffix="status", payload=json.dumps(status))
