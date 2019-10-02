#!/usr/bin/env python
# Nat Morris (c) 2019
"""CCTV buffer - Camera."""

import collections
import cv2
import imageio
import io
import logging
import sys
import threading
import time

LOG = logging.getLogger(__name__)


class Camera(object):

    def __init__(self, id, url, name=None):
        self.id = id
        if name is None:
            self.name = id
        else:
            self.name = name
        self.url = url
        self.queue = collections.deque()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=CameraWorker, kwargs={'url': self.url, 'lock': self.lock, 'id': self.id, 'queue': self.queue})
        self.started = False

    def start(self):
        self.thread.start()
        self.started = True

    def stop(self):
        pass

    def state_summary(self):
        with self.lock:
            state = {
                "id": self.id,
                "name": self.name,
                "started": self.started,
                "queuelen": len(self.queue)
            }
            if len(self.queue) > 0:
                state["last"] = int(self.queue[0][2])
                state["fps"] = self.queue[0][1]

        LOG.info("return state %s", state)
        return state


def CameraWorker(url, id, lock, queue):
    cap = cv2.VideoCapture(url)
    fps = cap.get(cv2.CAP_PROP_FPS)
    LOG.info("%s %s", id, fps)
    success, frame = cap.read()
    multipler = fps * 0.2

    while success:
        framenum = int(round(cap.get(1)))
        success, frame = cap.read()
        if framenum % multipler == 0:
            with lock:
                queue.append((frame, fps, time.time()))
                if len(queue) > 30:
                    queue.popleft()

    cap.release()