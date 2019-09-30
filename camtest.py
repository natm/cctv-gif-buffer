#!/usr/bin/env python3

import cherrypy
import collections
import cv2
import logging
import threading
import time
from jinja2 import Environment, FileSystemLoader

LOG = logging.getLogger(__name__)


def version():
    return "2.0.0"


class Camera(object):

    def __init__(self, id, url, name=None):
        self.id = id
        if name is None:
            self.name = id
        else:
            self.name = name
        self.url = url
        self.fps = None
        self.queue = collections.deque()
        self.lock = threading.Lock()

    def start(self):
        pass


class WebAppAdmin(object):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice
        self.env = Environment(loader=FileSystemLoader('templates'))

    @cherrypy.expose()
    def index(self):
        tmpl = self.env.get_template('admin/index.html')
        return tmpl.render(cameras=self.bufferservice.cameras, version=version())


class WebAppPublic(object):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice

    @cherrypy.expose()
    def index(self):
        return ""


class WebServer(threading.Thread):

    def __init__(self, bufferservice):
        threading.Thread.__init__(self)
        self.sync = threading.Condition()
        self.bufferservice = bufferservice

    def run(self):
        LOG.info("In run")
        cherrypy.tree.mount(WebAppPublic(bufferservice=self.bufferservice), '/')
        cherrypy.tree.mount(WebAppAdmin(bufferservice=self.bufferservice), '/admin')
        with self.sync:
            cherrypy.server.socket_port = 8001
            cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        with self.sync:
            cherrypy.engine.exit()
            cherrypy.engine.stop()


class BufferService(object):

    def __init__(self):
        self._cameras = []
        self._tokens = []
        self._webserver = WebServer(bufferservice=self)

    @property
    def cameras(self):
        return sorted(self._cameras, key=lambda cam: cam.name)

    @property
    def webserver(self):
        return self._webserver

    def add_camera(self, id, url, name=None):
        # check duplicate name/url is not already present
        self._cameras.append(Camera(id=id, name=name, url=url))

    def add_token(self, token):
        if token in self._tokens:
            LOG.warn("Skipping duplicate token %s", token)
        else:
            self._tokens.append(token)

    def setup_mqtt(self):
        pass

    def startcameras(self):
        pass


def main():

    logging.basicConfig(level=logging.INFO, format='%(levelname)8s [%(asctime)s] %(message)s')

    LOG.info(f"cctv-gif-buffer v{version()} starting")

    bs = BufferService()
    bs.add_camera(id="ch8", url="x")
    bs.add_camera(id="ch9", url="x")
    bs.add_camera(id="ch6", url="x")
    bs.add_token(token="abc")

    bs.setup_mqtt()

    for camera in bs.cameras:
        LOG.info(camera.name)

    # start webserver
    bs.webserver.start()

    LOG.info("Entering endless loop")
    while True:
        time.sleep(1)

    cap = cv2.VideoCapture('url')
    fps = cap.get(cv2.CAP_PROP_FPS)
    success, frame = cap.read()
    multipler = fps * 0.5

    maxpos = 10
    pos = 0

    while success:
        framenum = int(round(cap.get(1)))
        success, frame = cap.read()
        print('%s %s' % (framenum, multipler))
        if framenum % multipler == 0:
            print('writing')
            cv2.imwrite('test.jpg', frame)

    cap.release()


if __name__ == "__main__":
    main()
