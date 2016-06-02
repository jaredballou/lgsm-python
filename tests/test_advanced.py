# -*- coding: utf-8 -*-

from .context import *

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_load_config(self):
        conf = lgsm.GameConfig('insserver')
        pprint(conf.config)
        pprint(conf.dump_config(''))


if __name__ == '__main__':
    unittest.main()
