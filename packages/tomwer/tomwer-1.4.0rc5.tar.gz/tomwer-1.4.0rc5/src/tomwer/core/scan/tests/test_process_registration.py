# coding: utf-8
from __future__ import annotations

import shutil
import tempfile
import unittest

from tomoscan.io import HDF5File, get_swmr_mode

from tomwer.core.process.task import Task
from tomwer.core.utils.scanutils import MockNXtomo


class TestProcessRegistration(unittest.TestCase):
    """
    Make sure utils link to the process registration are
    correctly working
    """

    class DummyProcess(Task):
        @staticmethod
        def program_name():
            """Name of the program used for this processing"""
            return "dummy program"

        @staticmethod
        def program_version():
            """version of the program used for this processing"""
            return "0.0.0"

        @staticmethod
        def definition():
            """definition of the process"""
            return "no definition"

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.scan = MockNXtomo(scan_path=self.tmp_dir, n_proj=2).scan

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def testGetProcessNodes(self):
        """insure it return the last dark process based on the processing index"""

        for i in range(20):
            Task._register_process(
                self.scan.process_file,
                process=self.DummyProcess,
                entry=self.scan.entry,
                configuration=None,
                results={"output": i},
                process_index=i,
            )

        with HDF5File(self.scan.process_file, "r", swmr=get_swmr_mode()) as h5f:
            nodes = Task._get_process_nodes(
                root_node=h5f[self.scan.entry], process=self.DummyProcess
            )
            self.assertEqual(len(nodes), 20)
            self.assertTrue("/entry/tomwer_process_16" in nodes)
            self.assertEqual(nodes["/entry/tomwer_process_16"], 16)
            self.assertTrue("/entry/tomwer_process_1" in nodes)
            self.assertEqual(nodes["/entry/tomwer_process_1"], 1)
