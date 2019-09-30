#!/usr/bin/env python3

from cctvbuffer.archive.backends import BackendInterface


class B2(BackendInterface):

    required_envvars = ["B2_ACCOUNT_ID", "B2_ACCOUNT_KEY"]