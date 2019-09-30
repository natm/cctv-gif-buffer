#!/usr/bin/env python3

# following the same pattern as https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#

from cctvbuffer.archive.backends.b2 import B2
from cctvbuffer.archive.backends.local import Local
from cctvbuffer.archive.backends.s3 import S3


class BackendInterface(object):

    available_backends = [B2, Local, S3]