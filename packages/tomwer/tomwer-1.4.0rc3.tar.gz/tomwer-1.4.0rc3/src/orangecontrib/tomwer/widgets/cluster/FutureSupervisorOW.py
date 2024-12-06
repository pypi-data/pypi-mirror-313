from __future__ import annotations

import time

from orangewidget import gui

# from orangewidget.widget import Input, Output, OWBaseWidget
from orangecontrib.tomwer.orange.managedprocess import TomwerWithStackStack
from ewokscore.missing_data import MISSING_DATA
from ewoksorange.gui.orange_imports import Input

from processview.core.manager import DatasetState, ProcessManager
from processview.core.superviseprocess import SuperviseProcess
from silx.gui import qt
from silx.gui.utils.concurrent import submitToQtMainThread

from tomwer.core.futureobject import FutureTomwerObject
from tomwer.gui.cluster.supervisor import (
    FutureTomwerScanObserverWidget as _FutureTomwerScanObserverWidget,
)
from tomwer.core.process.cluster.supervisor import FutureSupervisorTask


class FutureSupervisorOW(
    TomwerWithStackStack,
    ewokstaskclass=FutureSupervisorTask,
):
    """
    Orange widget to define a slurm cluster as input of other
    widgets (based on nabu for now)
    """

    name = "future supervisor"
    id = "orange.widgets.tomwer.cluster.FutureSupervisorOW.FutureSupervisorOW"
    description = "Observe slurm job registered."
    icon = "icons/slurmobserver.svg"
    priority = 22
    keywords = [
        "tomography",
        "tomwer",
        "slurm",
        "observer",
        "cluster",
        "job",
        "sbatch",
        "supervisor",
        "future",
    ]

    want_main_area = True
    want_control_area = False
    resizing_enabled = True

    class Inputs:
        # redefine the input to allow multiple and default
        future_tomo_obj = Input(
            name="future_tomo_obj",
            type=FutureTomwerObject,
            doc="data with some remote processing",
            multiple=True,
            default=True,
        )

    def __init__(self, parent=None):
        super().__init__(parent)
        # gui
        layout = gui.vBox(self.mainArea, self.name).layout()
        self._widget = FutureTomwerObjectObserverWidget(
            parent=self, name=self.windowTitle()
        )
        layout.addWidget(self._widget)

        # connect signal / slot
        self._widget.observationTable.model().sigStatusUpdated.connect(
            self._convertBackAutomatically
        )
        self._widget.sigConversionRequested.connect(self._convertBack)

    def convertWhenFinished(self):
        return self._widget.convertWhenFinished()

    def _convertBackAutomatically(self, future_tomo_obj, status):
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_tomo_obj is expected to be an instance of {FutureTomwerObject} and not {type(future_tomo_obj)}"
            )
        if status in ("finished", "completed") and self.convertWhenFinished():
            self._convertBack(future_tomo_obj)

    def _convertBack(self, future_tomo_obj):
        if not isinstance(future_tomo_obj, FutureTomwerObject):
            raise TypeError(
                f"future_tomo_obj is expected to be an instance of {FutureTomwerObject} and not {type(future_tomo_obj)}"
            )
        self._widget.removeFutureTomoObj(future_tomo_obj=future_tomo_obj)
        self.execute_ewoks_task()

    def handleNewSignals(self) -> None:
        """Invoked by the workflow signal propagation manager after all
        signals handlers have been called.

        note: this widget can receive two signals: 'dataset' and 'colormap'. The 'colormap' is handled by
              orange directly while the 'dataset' signal is handled by the ewoks task.
              This function will be only triggered when the 'dataset' signal is send
        """
        # update GUI from received future_tomo_obj
        # warning: this code will work because the task has only one input.
        # so we can pass it directly to the widget.
        # this won't be the case the task can have several input.
        future_tomo_obj = self.get_task_input_value("future_tomo_obj", MISSING_DATA)
        if future_tomo_obj is not MISSING_DATA:
            self._widget.addFutureTomoObj(future_tomo_obj=future_tomo_obj)

    @Inputs.future_tomo_obj
    def add(self, future_tomo_obj, signal_id=None):
        # required because today ewoksorange is not handling multiple inputs
        self.set_dynamic_input("future_tomo_obj", future_tomo_obj)


class FutureTomwerObjectObserverWidget(
    _FutureTomwerScanObserverWidget, SuperviseProcess
):
    """add dataset state notification (ProcessManager) to the original FutureTomwerScanObserverWidget"""

    REFRESH_FREQUENCE = 10
    """time between call to updateView"""

    def __init__(self, name, parent=None):
        super().__init__(parent=parent)
        self.name = name
        self._updateThread = _RefreshThread(
            callback=self.updateView, refresh_frequence=self.REFRESH_FREQUENCE
        )
        self.destroyed.connect(self.stopRefresh)
        self._updateThread.start()

    def stopRefresh(self):
        if self._updateThread is not None:
            self._updateThread.stop()
            self._updateThread.wait(self.REFRESH_FREQUENCE + 1)
            self._updateThread = None

    def close(self):
        self.stopRefresh()
        super().close()

    def addFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        super().addFutureTomoObj(future_tomo_obj)
        self._updateTomoObjSupervisor(future_tomo_obj)

    def removeFutureTomoObj(self, future_tomo_obj: FutureTomwerObject):
        self._updateTomoObjSupervisor(future_tomo_obj)
        super().removeFutureTomoObj(future_tomo_obj)

    def _updateTomoObjSupervisor(self, future_tomo_obj):
        r_id = future_tomo_obj.process_requester_id
        if r_id is not None:
            requester_name = ProcessManager().get_process(r_id).name
        else:
            requester_name = "unknow"
        details = f"job spawn by {requester_name}"
        if future_tomo_obj is None:
            return
        elif future_tomo_obj.status == "error":
            state = DatasetState.FAILED
        elif future_tomo_obj.status == "pending":
            details = "\n".join([details, "pending"])
            state = DatasetState.PENDING
        elif future_tomo_obj.status in ("finished", "completed"):
            details = future_tomo_obj.logs or "no log found"
            state = DatasetState.SUCCEED
        elif future_tomo_obj.status == "running":
            details = "\n".join([details, "running"])
            state = DatasetState.ON_GOING
        elif future_tomo_obj.status == "cancelled":
            details = "\n".join([details, "job cancelled"])
            state = DatasetState.SKIPPED
        elif future_tomo_obj.status is None:
            return
        else:
            raise ValueError(
                f"future scan status '{future_tomo_obj.status}' is not managed, {type(future_tomo_obj.status)}"
            )
        ProcessManager().notify_dataset_state(
            dataset=future_tomo_obj.tomo_obj,
            process=self,
            state=state,
            details=details,
        )

    def _updateStatus(self, future_tomo_obj):
        self._updateTomoObjSupervisor(future_tomo_obj)
        super()._updateStatus(future_tomo_obj)


class _RefreshThread(qt.QThread):
    """Simple thread to call a refresh callback each refresh_frequence (seconds)"""

    TIME_BETWEEN_LOOP = 1.0

    def __init__(self, callback, refresh_frequence) -> None:
        super().__init__()
        self._callback = callback
        self._refresh_frequence = refresh_frequence
        self._stop = False

    def stop(self):
        self._stop = True
        self._callback = None

    def run(self):
        w_t = self._refresh_frequence + self.TIME_BETWEEN_LOOP

        while not self._stop:
            if w_t <= 0:
                if self._callback is not None:
                    try:
                        submitToQtMainThread(self._callback)
                    except AttributeError:
                        # can happen when closing
                        pass
                w_t = self._refresh_frequence + self.TIME_BETWEEN_LOOP
            w_t -= self.TIME_BETWEEN_LOOP
            time.sleep(self.TIME_BETWEEN_LOOP)
