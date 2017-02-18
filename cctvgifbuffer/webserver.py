#!/usr/bin/env python
# Nat Morris (c) 2017

import cherrypy
import copy
import imageio
from cctvgifbuffer import version


class WebServer(object):

    service = None

    def __init__(self, service):
        self.service = service

    @cherrypy.expose
    def index(self):
        return "cctv-gif-buffer v%s" % (version())

    @cherrypy.expose
    def gif(self, camera):
        if camera not in self.service.cameras.keys():
            raise cherrypy.HTTPError(404, "Camera not found")
        camobject = self.service.cameras[camera]
        # obtain a temporary lock to copy the buffer
        with camobject["lock"]:
            x = copy.copy(camobject["buffer"])
        imageio.mimsave("test.gif", x, 'GIF', duration=2)
        return self.service.cameras.keys()

    def start(self):
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.quickstart(self)
