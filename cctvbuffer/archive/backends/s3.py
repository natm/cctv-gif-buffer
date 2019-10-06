#!/usr/bin/env python3

from cctvbuffer.archive.backends.interface import BackendInterface


class S3(BackendInterface):

    required_envvars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]