#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.main_base import LicompParser

from licomp_reclicense.config import cli_name
from licomp_reclicense.config import description
from licomp_reclicense.config import epilog
from licomp_reclicense.reclicense import LicompReclicense

def main():
    lr = LicompReclicense()
    o_parser = LicompParser(lr,
                            cli_name,
                            description,
                            epilog,
                            UseCase.LIBRARY,
                            Provisioning.BIN_DIST)
    o_parser.run()


if __name__ == '__main__':
    main()
