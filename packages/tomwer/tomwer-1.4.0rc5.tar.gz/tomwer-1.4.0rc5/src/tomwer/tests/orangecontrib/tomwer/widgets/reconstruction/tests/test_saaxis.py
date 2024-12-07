# coding: utf-8
from __future__ import annotations

import gc
import logging
import os
import pickle
import shutil
import tempfile
import time
import uuid

import h5py
import numpy
from orangecanvas.scheme.readwrite import literal_dumps
from processview.core.manager import DatasetState, ProcessManager
from silx.gui import qt
from silx.gui.utils.testutils import TestCaseQt
from silx.io.url import DataUrl

from orangecontrib.tomwer.widgets.reconstruction.SAAxisOW import SAAxisOW as _SAAxisOW
from tomwer.core import settings
from tomwer.core.utils.lbsram import mock_low_memory
from tomwer.core.process.reconstruction.scores import ComputedScore
from tomwer.core.utils.scanutils import MockNXtomo

logger = logging.getLogger(__name__)


class SAAxisOW(_SAAxisOW):
    def __init__(self, parent=None):
        self._scans_finished = []
        super().__init__(parent)

    def processing_finished(self, scan):
        # TODO: add message processing finished
        self._scans_finished.append(scan)

    @property
    def scans_finished(self):
        return self._scans_finished

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

        self.widget = SAAxisOW()
        self.widget.show()

        def patch_score(*args, **kwargs):
            data = numpy.random.random(TestProcessing.DIM * TestProcessing.DIM)
            data = data.reshape(TestProcessing.DIM, TestProcessing.DIM)
            slice_file_path = os.path.join(
                self._source_dir, str(uuid.uuid1()) + ".hdf5"
            )
            data_url = DataUrl(
                file_path=slice_file_path, data_path="data", scheme="silx"
            )
            with h5py.File(slice_file_path, mode="a") as h5f:
                h5f["data"] = data
            return data_url, ComputedScore(
                tv=numpy.random.random(),
                std=numpy.random.random(),
            )

        self.widget._widget._processing_stack.patch_processing(patch_score)

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
        literal_dumps(self.widget.getConfiguration())

    def testAutoFocusUnlock(self):
        self.widget.lockAutofocus(False)

        def manual_processing():
            self.widget.load_sinogram()
            self.widget.compute()
            self.qapp.processEvents()
            self.widget.wait_processing(5000)
            self.qapp.processEvents()

        self.widget.process(self.scan_1)
        manual_processing()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_1.get_identifier(),
                process=self.widget,
            ),
            DatasetState.WAIT_USER_VALIDATION,
        )

        self.widget.process(self.scan_2)
        manual_processing()
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
        manual_processing()
        self.widget.validateCurrentScan()
        self.assertEqual(
            self._process_manager.get_dataset_state(
                dataset_id=self.scan_3.get_identifier(),
                process=self.widget,
            ),
            DatasetState.SUCCEED,
        )
        # insure a cor has been registered
        self.assertNotEqual(self.scan_3.axis_params.relative_cor_value, None)

    def testTestLbsram(self):
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

    def testAutoFocusLock(self):
        self.widget.lockAutofocus(True)
        for scan in (self.scan_1, self.scan_2, self.scan_3):
            self.widget.process(scan)
            self.widget.wait_processing(10000)
            self.qapp.processEvents()
            time.sleep(0.1)
            self.qapp.processEvents()
            self.assertEqual(
                self._process_manager.get_dataset_state(
                    dataset_id=scan.get_identifier(),
                    process=self.widget,
                ),
                DatasetState.SUCCEED,
            )
