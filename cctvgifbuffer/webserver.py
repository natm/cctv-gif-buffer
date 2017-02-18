#!/usr/bin/env python
# Nat Morris (c) 2017
"""CCTV GIF buffer - WebServer."""

import cherrypy
import copy
import imageio
import io
from cctvgifbuffer import version


class WebServer(object):

    service = None

    def __init__(self, service):
        self.service = service

    @cherrypy.expose
    def index(self):
        return "cctv-gif-buffer v%s" % (version())

    @cherrypy.expose
    def gif(self, camera, duration, interval):
        # sanitize the parameters
        if camera not in self.service.cameras.keys():
            raise cherrypy.HTTPError(404, "Camera not found")
        duration = int(duration)
        if duration != 60:
            raise cherrypy.HTTPError(500, "Only 60 second duration is currently supported")
        interval = float(interval)
        valid_intervals = [0.25, 0.5, 1]
        if interval not in valid_intervals:
            raise cherrypy.HTTPError(500, "Support frame intervals are %s" % (valid_intervals))
        camobject = self.service.cameras[camera]
        # obtain a temporary lock to copy the buffer
        with camobject["lock"]:
            x = copy.copy(camobject["buffer"])
        # generate the GIF
        outbytes = imageio.mimsave(imageio.RETURN_BYTES, x, 'GIF', duration=interval)
        # serve it to the user
        cherrypy.response.headers['Content-Type'] = 'image/gif'
        return io.BytesIO(outbytes)

    def start(self):
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.server.socket_port = 8080
        cherrypy.quickstart(self)
