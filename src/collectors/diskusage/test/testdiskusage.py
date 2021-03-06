#!/usr/bin/python
# coding=utf-8
################################################################################

from __future__ import with_statement

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch
from contextlib import nested

from diamond.collector import Collector
from diskusage import DiskUsageCollector

################################################################################


class TestDiskUsageCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('DiskUsageCollector', {
            'interval': 10,
            'sector_size': '512',
            'byte_unit': 'kilobyte'
        })

        self.collector = DiskUsageCollector(config, None)

    @patch('os.access', Mock(return_value=True))
    def test_get_disk_statistics(self):
        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('diskstats')))):

            result = self.collector.get_disk_statistics()

            open.assert_called_once_with('/proc/diskstats')

        self.assertEqual(
            sorted(result.keys()),
            [(8,  0), (8,  1), (8, 16), (8, 17), (8, 32),
                (8, 33), (8, 48), (8, 49), (9,  0)])

        return result

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = self.getPickledResults('test_should_work_with_real_data.pkl')
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_vda_and_xvdb(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_vda_xvdb'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_vda_xvdb'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = self.getPickledResults(
            'test_verify_supporting_vda_and_xvdb.pkl')
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_md_dm(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_md_dm'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_md_dm'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = self.getPickledResults('test_verify_supporting_md_dm.pkl')
        self.assertPublishedMany(publish_mock, metrics)

    @patch('os.access', Mock(return_value=True))
    @patch.object(Collector, 'publish')
    def test_verify_supporting_disk(self, publish_mock):

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_1_disk'))),
                patch('time.time', Mock(return_value=10))):
            self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with nested(
            patch('__builtin__.open', Mock(
                return_value=self.getFixture('proc_diskstats_2_disk'))),
                patch('time.time', Mock(return_value=20))):
            self.collector.collect()

        metrics = self.getPickledResults('test_verify_supporting_disk.pkl')
        self.assertPublishedMany(publish_mock, metrics)


################################################################################
if __name__ == "__main__":
    unittest.main()
