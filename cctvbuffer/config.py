#!/usr/bin/env python3

import logging
import sys

LOG = logging.getLogger(__name__)


def validate(config):

    if type(config) is not dict:
        LOG.fatal("Invalid YAML config")
        sys.exit(1)

    return True