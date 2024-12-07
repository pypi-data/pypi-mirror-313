#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

from licomp.interface import UseCase
from licomp.interface import Provisioning
from licomp.main_base import LicompParser

from licomp_dwheeler.config import cli_name
from licomp_dwheeler.config import description
from licomp_dwheeler.config import epilog
from licomp_dwheeler.dwheeler import LicompDw

def main():
    ld = LicompDw()
    o_parser = LicompParser(ld,
                            cli_name,
                            description,
                            epilog,
                            UseCase.LIBRARY,
                            Provisioning.BIN_DIST)
    o_parser.run()


if __name__ == '__main__':
    main()
