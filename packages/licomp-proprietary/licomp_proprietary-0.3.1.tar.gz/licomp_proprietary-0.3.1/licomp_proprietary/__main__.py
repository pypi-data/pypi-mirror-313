#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.main_base import LicompParser

from licomp_proprietary.config import cli_name
from licomp_proprietary.config import description
from licomp_proprietary.config import epilog
from licomp_proprietary.proprietary import LicompProprietary

def main():
    lp = LicompProprietary()
    o_parser = LicompParser(lp,
                            cli_name,
                            description,
                            epilog,
                            UseCase.LIBRARY,
                            Provisioning.BIN_DIST)
    o_parser.run()


if __name__ == '__main__':
    main()
