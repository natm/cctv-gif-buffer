#!/usr/bin/env python
# Nat Morris (c) 2019
"""CCTV buffer - Service."""

import cherrypy
import copy
import cv2
import imageio
import io
import logging
import threading
from jinja2 import Environment, FileSystemLoader
from cctvbuffer import version

LOG = logging.getLogger(__name__)


class WebAppAdmin(object):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice
        self.env = Environment(loader=FileSystemLoader('templates'))

    @cherrypy.expose()
    def index(self):
        tmpl = self.env.get_template('admin_index.html')
        return tmpl.render(cameras=self.bufferservice.cameras, version=version())


class WebAppPublic(object):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice

    @cherrypy.expose()
    def index(self, ch):
        camera = None
        for c in self.bufferservice.cameras:
            if c.id == ch:
                camera = c
        if camera is None:
            return "Camera not found"
        with camera.lock:
            x = copy.copy(camera.queue)
        y = []
        for frame in x:
            jpg = cv2.imencode('.jpg', frame[0])[1]
            y.append(imageio.imread(io.BytesIO(jpg)))

        outbytes = imageio.mimsave(imageio.RETURN_BYTES, y, 'GIF', fps=4)
        cherrypy.response.headers['Content-Type'] = 'image/gif'
        return io.BytesIO(outbytes)


class WebServer(threading.Thread):

    def __init__(self, bufferservice):
        self.bufferservice = bufferservice
        threading.Thread.__init__(self)
        self.sync = threading.Condition()

    def run(self):
        LOG.info("In run")
        cherrypy.tree.mount(WebAppPublic(bufferservice=self.bufferservice), '/')
        cherrypy.tree.mount(WebAppAdmin(bufferservice=self.bufferservice), '/admin')
        with self.sync:
            cherrypy.config.update({
                'global': {
                    'engine.autoreload.on': False
                }
            })
            cherrypy.server.socket_port = 8001
            cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        with self.sync:
            cherrypy.engine.exit()
            cherrypy.engine.stop()
