#!/usr/bin/env python
# Nat Morris (c) 2017, 2019

import argparse
import logging
import os
import signal
import sys
import yaml

from cctvbuffer import version
from cctvbuffer.config import validate
from cctvbuffer.service import BufferService

LOG = logging.getLogger(__name__)


def main():

    logging.basicConfig(level=logging.INFO, format='%(levelname)8s [%(asctime)s] %(message)s')

    parser = argparse.ArgumentParser(description="CCTV Buffer")
    parser.add_argument("-c", "--config", help="Config file", required=True)
    parser.add_argument("-v", "--verbose", help="Increase verbosity", action="store_true")
    args = parser.parse_args()

    LOG.info("CCTV Buffer v%s", version())

    # check config exists
    cfgpath = args.config.strip()
    if os.path.isfile(cfgpath) is False:
        LOG.fatal("Specified config file does not exist: %s", cfgpath)
        sys.exit(1)

    # load the config
    with open(cfgpath, 'r') as stream:
        try:
            config = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    validate(config=config)

    svc = BufferService(config=config)
    svc.start()

    sys.exit(0)


if __name__ == "__main__":
    main()
