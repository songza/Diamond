#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import patch

from diamond.collector import Collector
from users import UsersCollector

import sys


################################################################################

def run_only(func, predicate):
    if predicate():
        return func
    else:
        def f(arg):
            pass
        return f


def run_only_if_pyutmp_is_available(func):
    try:
        import pyutmp
        pyutmp  # workaround for pyflakes issue #13
    except ImportError:
        pyutmp = None
    pred = lambda: pyutmp is not None
    return run_only(func, pred)


class TestUsersCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('UsersCollector', {
            'utmp': self.getFixturePath('utmp.centos6'),
        })

        self.collector = UsersCollector(config, None)

    @run_only_if_pyutmp_is_available
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        metrics = {
            'kormoc':   2,
            'root':     3,
            'total':    5,
        }

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

        # Because of the compiled nature of pyutmp, we can't actually test
        # different operating system versions then the currently running
        # one
        if sys.platform.startswith('linux'):
            self.collector.collect()

            self.assertPublishedMany(publish_mock, metrics)

################################################################################
if __name__ == "__main__":
    unittest.main()
