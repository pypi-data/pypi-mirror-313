# coding: utf-8
from __future__ import annotations

import gc
import logging
import os
import pickle
import shutil
import tempfile

from orangecanvas.scheme.readwrite import literal_dumps
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.io.utils import h5py_read_dataset

from orangecontrib.tomwer.widgets.reconstruction.SinoNormOW import (
    SinoNormOW as _NormIOW,
)
from tomwer.core import settings
from tomwer.core.utils.lbsram import mock_low_memory
from tomwer.core.process.reconstruction.normalization import SinoNormalizationTask
from tomwer.core.utils.scanutils import MockNXtomo
from tomwer.io.utils.h5pyutils import EntryReader

logger = logging.getLogger(__name__)


class NormIOW(_NormIOW):
    def __init__(self, parent=None):
        self._scans_finished = []
        super().__init__(parent)

    def processing_finished(self, scan):
        self._scans_finished.append(scan)

    def wait_processing(self, wait_time):
        self._window._processing_stack._computationThread.wait(wait_time)

    @property
    def scans_finished(self):
        return self._scans_finished

    def compute(self):
        self._window._processCurrentScan()

    def setROI(self, start_x, end_x, start_y, end_y):
        self._window.setROI(start_x=start_x, end_x=end_x, start_y=start_y, end_y=end_y)

    def close(self):
        self._scans_finished = {}
        super().close()


class TestProcessing(TestCaseQt):
    DIM = 100

    def setUp(self):
        super().setUp()
        self._source_dir = tempfile.mkdtemp()

        def create_scan(folder_name):
            _dir = os.path.join(self._source_dir, folder_name)
            return MockNXtomo(
                scan_path=_dir,
                n_ini_proj=20,
                n_proj=20,
                n_alignement_proj=2,
                create_final_flat=False,
                create_ini_dark=True,
                create_ini_flat=True,
                n_refs=1,
                dim=self.DIM,
            ).scan

        # create scans
        self.scan_1 = create_scan("scan_1")
        self.scan_2 = create_scan("scan_2")
        self.scan_3 = create_scan("scan_3")
        self._process_manager = ProcessManager()

        self.widget = NormIOW()
        self.widget.show()

    def tearDown(self):
        mock_low_memory(False)
        settings.mock_lsbram(False)
        self.widget.setAttribute(qt.Qt.WA_DeleteOnClose)
        self.widget.close()
        self.widget = None
        self.qapp.processEvents()
        shutil.rmtree(self._source_dir)
        gc.collect()

    def test_serializing(self):
        pickle.dumps(self.widget.getConfiguration())

    def test_literal_dumps(self):
        self.widget._updateSettings()
        literal_dumps(self.widget._ewoks_default_inputs)

    def testUnlocked(self):
        """Test result when used with some interaction"""
        self.widget.setLocked(False)

        def process_scalar_manually():
            self.widget.setCurrentMethod("division")
            self.widget.setCurrentSource("manual ROI")

            self.qapp.processEvents()
            self.widget.setROI(start_x=0, end_x=10, start_y=0, end_y=10)
            self.qapp.processEvents()
            self.widget.compute()
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        self.widget.process(self.scan_1)
        process_scalar_manually()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_1.get_identifier(),
                process=self.widget,
            ),
            DatasetState.WAIT_USER_VALIDATION,
        )

        self.widget.process(self.scan_2)
        process_scalar_manually()
        self.assertEqual(len(self.widget.scans_finished), 0)
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_1.get_identifier(),
                process=self.widget,
            ),
            DatasetState.SKIPPED,
        )
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_2.get_identifier(),
                process=self.widget,
            ),
            DatasetState.WAIT_USER_VALIDATION,
        )

        self.widget.process(self.scan_3)
        process_scalar_manually()
        self.widget.validateCurrentScan()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_3.get_identifier(),
                process=self.widget,
            ),
            DatasetState.SUCCEED,
        )

    def testTestLbsram(self):
        """Test scan are all validated if 'low memory on lbsram' scenario is
        activated"""
        mock_low_memory(True)
        settings.mock_lsbram(True)
        for scan in (self.scan_1, self.scan_2, self.scan_3):
            self.widget.process(scan)
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        for scan in (self.scan_1, self.scan_2, self.scan_3):
            with self.subTest(scan=str(scan)):
                self.assertEqual(
                    self._process_manager.get_dataset_state(
                        dataset_id=scan.get_identifier(),
                        process=self.widget,
                    ),
                    DatasetState.SKIPPED,
                )

    def testLocked(self):
        """Test scan are all validated if the widget is lock"""
        self.widget.setLocked(True)
        for scan in (self.scan_1, self.scan_2, self.scan_3):
            self.widget.process(scan)
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        for scan in (self.scan_1, self.scan_2, self.scan_3):
            # test status is SUCCEED
            with self.subTest(scan=str(scan)):
                self.assertEqual(
                    self._process_manager.get_dataset_state(
                        dataset_id=scan.get_identifier(),
                        process=self.widget,
                    ),
                    DatasetState.SUCCEED,
                )
            # test process file has been updated
            with EntryReader(scan.process_file_url) as entry:
                self.assertTrue("tomwer_process_0" in entry)
                self.assertEqual(
                    h5py_read_dataset(entry["tomwer_process_0"]["program"]),
                    SinoNormalizationTask.program_name(),
                )
