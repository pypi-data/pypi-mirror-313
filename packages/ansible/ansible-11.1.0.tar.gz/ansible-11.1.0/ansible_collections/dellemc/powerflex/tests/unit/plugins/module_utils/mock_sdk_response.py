# Copyright: (c) 2022, Dell Technologies

# Apache License version 2.0 (see MODULE-LICENSE or http://www.apache.org/licenses/LICENSE-2.0.txt)

"""Mock SDKResponse for Unit tests for Dell Technologies (Dell) PowerFlex modules"""

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class MockSDKResponse:
    def __init__(self, data=None, status_code=200):
        self.data = data
        self.status_code = status_code
