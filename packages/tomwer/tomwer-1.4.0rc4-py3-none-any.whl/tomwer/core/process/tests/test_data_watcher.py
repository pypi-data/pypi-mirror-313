# coding: utf-8
from __future__ import annotations


import os
import time

import pytest

from tomwer.core.process.control.datawatcher import DataWatcher
from tomwer.core.process.control.datawatcher.status import DET_END_XML, PARSE_INFO_FILE
from tomwer.core.utils.scanutils import MockEDF
from tomwer.core.utils.threads import LoopThread


@pytest.mark.skipif(os.name != "posix", reason="not tested under windows yet")
@pytest.mark.parametrize("det_method", (PARSE_INFO_FILE, DET_END_XML))
def test_data_watcher_io(tmp_path, det_method):
    """Test inputs and outputs types of the handler functions"""
    scan_folder = tmp_path / "folder" / "my_scan"
    data_watcher_process = DataWatcher()
    data_watcher_process.setWaitTimeBtwLoop(1)
    data_watcher_process.setObsMethod(det_method)

    MockEDF.mockScan(
        scanID=str(scan_folder), nRadio=10, nRecons=1, nPagRecons=4, dim=10
    )
    data_watcher_process.setFolderObserved(str(tmp_path / "folder"))
    data_watcher_process.clear_output_values()
    data_watcher_process.set_serialize_output_data(True)
    LoopThread.quitEvent.clear()
    data_watcher_process.start()

    # note: this quitEvent is nasty. But we don't want to spend time on the (EDF) data watcher which is not the future

    timeout = 8
    while data_watcher_process.get_output_value("data") is None and timeout > 0:
        _delta = 0.5
        time.sleep(_delta)
        timeout -= _delta

    def quit_test():
        data_watcher_process.stop()
        data_watcher_process.waitForObservationFinished()
        import gc

        gc.collect()
        LoopThread.quitEvent.clear()

    if timeout <= 0:
        quit_test()
        raise TimeoutError("timeout expire")

    out = data_watcher_process.get_output_value("data")
    assert isinstance(out, dict)
    quit_test()
