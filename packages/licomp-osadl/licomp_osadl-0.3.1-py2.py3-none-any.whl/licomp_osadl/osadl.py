#!/bin/env python3

# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import logging

from licomp_osadl.config import module_name
from licomp_osadl.config import licomp_osadl_version
from licomp_osadl.config import my_supported_api_version
from licomp_osadl.config import disclaimer

from licomp.interface import Licomp
from licomp.interface import Provisioning
from licomp.interface import UseCase
from licomp.interface import CompatibilityStatus

SCRIPT_DIR = os.path.dirname(__file__)
MATRIX_FILE_NAME = 'matrixseqexpl.json'
MATRIX_DIR = os.path.join(SCRIPT_DIR, 'data')
MATRIX_FILE = os.path.join(MATRIX_DIR, MATRIX_FILE_NAME)


class LicompOsadl(Licomp):

    def __init__(self):
        Licomp.__init__(self)
        self.provisionings = [Provisioning.BIN_DIST]
        self.usecases = [UseCase.SNIPPET]
        logging.debug(f'Reading JSON file: {MATRIX_FILE}')

        with open(MATRIX_FILE) as fp:
            self.matrix = json.load(fp)
            self.licenses = {}
            for lic in self.matrix['licenses']:
                lic_name = lic['name']
                logging.debug(f'  * manage license: {lic_name}')
                self.licenses[lic_name] = {}
                for compat in lic['compatibilities']:
                    compat_name = compat['name']
                    new_compat = {}
                    new_compat['compatibility'] = compat['compatibility']
                    new_compat['explanation'] = compat['explanation']
                    self.licenses[lic_name][compat_name] = new_compat

        self.ret_statuses = {
            "Same": CompatibilityStatus.COMPATIBLE,
            "Yes": CompatibilityStatus.COMPATIBLE,
            "No": CompatibilityStatus.INCOMPATIBLE,
            "Unknown": CompatibilityStatus.UNKNOWN,
            "Check dependency": CompatibilityStatus.DEPENDS,
        }

    def name(self):
        return module_name

    def version(self):
        return licomp_osadl_version

    def supported_api_version(self):
        return my_supported_api_version

    def supported_licenses(self):
        return list(self.licenses.keys())

    def supported_usecases(self):
        return self.usecases

    def supported_provisionings(self):
        return self.provisionings

    def disclaimer(self):
        return disclaimer

    def _status_to_licomp_status(self, status):
        return self.ret_statuses[status]

    def _outbound_inbound_compatibility(self,
                                        outbound,
                                        inbound,
                                        usecase,
                                        provisioning,
                                        modified):
        result = self.licenses[outbound][inbound]
        compat = result['compatibility']
        compat_value = self.ret_statuses[compat]
        return self.outbound_inbound_reply(compat_value, result['explanation'])
