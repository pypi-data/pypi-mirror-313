#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os

from licomp_reclicense.config import module_name
from licomp_reclicense.config import version
from licomp_reclicense.config import my_supported_api_version
from licomp_reclicense.config import disclaimer

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
VAR_DIR = os.path.join(SCRIPT_DIR, 'data')
MATRIX_FILE_NAME = 'reclicense-matrix.json'
MATRIX_FILE = os.path.join(VAR_DIR, MATRIX_FILE_NAME)

class LicompReclicense(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.provisionings = [Provisioning.BIN_DIST, Provisioning.SOURCE_DIST]
        self.usecases = [UseCase.LIBRARY]
        with open(MATRIX_FILE) as fp:
            self.matrix = json.load(fp)
            self.licenses = self.matrix['licenses']

        self.ret_statuses = {
            "1": CompatibilityStatus.COMPATIBLE,
            "2": CompatibilityStatus.COMPATIBLE,
            "1,2": CompatibilityStatus.COMPATIBLE,
            "0": CompatibilityStatus.INCOMPATIBLE,
        }

    def _outbound_inbound_compatibility(self,
                                        outbound,
                                        inbound,
                                        usecase,
                                        provisionings,
                                        modification):

        values = self.licenses[outbound][inbound]

        return self.outbound_inbound_reply(self.ret_statuses[values],
                                           f'values from matrix: {values}')

    def name(self):
        return module_name

    def version(self):
        return version

    def supported_api_version(self):
        return my_supported_api_version

    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_usecases(self):
        return self.usecases

    def disclaimer(self):
        return disclaimer

    def supported_provisionings(self):
        return self.provisionings
