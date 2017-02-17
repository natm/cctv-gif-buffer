#!/usr/bin/env python
# Nat Morris (c) 2017

import argparse
import logging
import os
import signal
import sys
import io
import yaml

from cctvgifbuffer.service import Service


LOG = logging.getLogger(__name__)

def main():

    logging.basicConfig(level=logging.INFO, format='%(levelname)8s [%(asctime)s] %(message)s')

    parser = argparse.ArgumentParser(description="CCTV GIF Buffer")
    parser.add_argument("-c", "--config", help="Config file", required=True)
    parser.add_argument("-v", "--verbose", help="Increase verbosity", action="store_true")
    args = parser.parse_args()

    # check config exists
    cfgpath = os.path.abspath(args.config)
    if os.path.isfile(cfgpath) is False:
        LOG.fail("Specified config file does not exist: %s", cfgpath)
        sys.exit(1)

    # load the config
    with open(cfgpath, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    if type(config) is not dict:
        LOG.fail("Invalid YAML config")
        sys.exit(1)

    svc = Service(config=config)
    svc.start()

    sys.exit(0)


if __name__ == "__main__":
    main()
