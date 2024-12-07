from __future__ import annotations

import logging
import weakref

import numpy
from silx.gui import qt

from nxtomo.nxobject.nxdetector import ImageKey, FOV
from nxtomo.utils.transformation import build_matrix

from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorTask, NXtomoEditorKeys
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.gui.utils.scandescription import ScanNameLabelAndShape
from tomwer.gui.utils.unitsystem import MetricEntry
from tomwer.gui.edit.nxtomowarmer import NXtomoProxyWarmer

_logger = logging.getLogger(__name__)


class NXtomoEditorDialog(qt.QDialog):
    """
    Dialog embedding instances of NXtomoEditor and NXtomoProxyWarmer
    """

    def __init__(self, parent=None, hide_lockers=True) -> None:
        super().__init__(parent)
        self.setLayout(qt.QVBoxLayout())

        self.mainWidget = NXtomoEditor(parent=self, hide_lockers=hide_lockers)
        self.layout().addWidget(self.mainWidget)
        self._warmer = NXtomoProxyWarmer(parent=self)
        self.layout().addWidget(self._warmer)

        types = qt.QDialogButtonBox.Ok
        self._buttons = qt.QDialogButtonBox(parent=self)
        self._buttons.setStandardButtons(types)
        self._buttons.button(qt.QDialogButtonBox.Ok).setText("validate")
        self.layout().addWidget(self._buttons)

    # expose API
    def setScan(self, scan: NXtomoScan) -> None:
        self.mainWidget.setScan(scan)
        self._warmer.setScan(scan)

    def hasLockField(self) -> bool:
        return self.mainWidget.hasLockField()

    def getConfiguration(self) -> dict:
        return self.mainWidget.getConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self.mainWidget.setConfiguration(config)

    def getConfigurationForTask(self) -> dict:
        return self.mainWidget.getConfigurationForTask()


class NXtomoEditor(qt.QWidget):
    """
    Widget to edit a set of field from a NXtomo.
    The preliminary goal is to let the user define pixel / voxel position and x and z positions
    in order to simplify stitching down the line

    As energy and field of view was also often requested this part is also editable.

    Each field contains a widget to define it values and a LockButton. The LockButton can be used to automate the
    processing.

    When the scan to edit is set each field widget will be updated **at the condition** the field is not locked.
    Else existing value will be kept.
    """

    sigEditingFinished = qt.Signal()
    """emit when edition is finished"""

    def __init__(self, parent=None, hide_lockers=True):
        super().__init__(parent)
        self._editableWidgets = []
        self._lockerPBs = []
        # list of all lockers
        self._scan = None
        self.setLayout(qt.QVBoxLayout())
        self._scanInfoQLE = ScanNameLabelAndShape(parent=self)
        self.layout().addWidget(self._scanInfoQLE)

        # nxtomo tree
        self._tree = qt.QTreeWidget(self)
        if hide_lockers:
            self._tree.setColumnCount(2)
            self._tree.setHeaderLabels(("entry", "value"))
        else:
            self._tree.setColumnCount(3)
            self._tree.setHeaderLabels(("entry", "value", "lockers"))
            self._tree.header().setStretchLastSection(False)
            self._tree.setColumnWidth(2, 20)
            self._tree.header().setSectionResizeMode(1, qt.QHeaderView.Stretch)
        self.layout().addWidget(self._tree)

        # 1: instrument
        self._instrumentQTWI = qt.QTreeWidgetItem(self._tree)
        self._instrumentQTWI.setText(0, "instrument")
        # handle energy
        self._beamQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._beamQTWI.setText(0, "beam")
        self._energyQTWI = qt.QTreeWidgetItem(self._beamQTWI)
        self._energyQTWI.setText(0, "energy (keV)")
        self._energyEntry = EnergyEntry("", self)
        self._energyEntry.setPlaceholderText("energy in kev")
        self._tree.setItemWidget(self._energyQTWI, 1, self._energyEntry)
        self._editableWidgets.append(self._energyEntry)
        self._energyLockerLB = PadlockButton(self)
        self._energyLockerLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._energyLockerLB)
        self._tree.setItemWidget(self._energyQTWI, 2, self._energyLockerLB)

        # 1.1 detector
        self._detectorQTWI = qt.QTreeWidgetItem(self._instrumentQTWI)
        self._detectorQTWI.setText(0, "detector")
        ## pixel size
        self._xPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._xPixelSizeQTWI.setText(0, "x pixel size")
        self._xPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._xPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(self._xPixelSizeQTWI, 1, self._xPixelSizeMetricEntry)
        self._editableWidgets.append(self._xPixelSizeMetricEntry)
        self._xPixelSizeLB = PadlockButton(self)
        self._xPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xPixelSizeLB)
        self._tree.setItemWidget(self._xPixelSizeQTWI, 2, self._xPixelSizeLB)

        self._yPixelSizeQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._yPixelSizeQTWI.setText(0, "y pixel size")
        self._yPixelSizeMetricEntry = MetricEntry("", parent=self)
        self._yPixelSizeMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(self._yPixelSizeQTWI, 1, self._yPixelSizeMetricEntry)
        self._editableWidgets.append(self._yPixelSizeMetricEntry)
        self._yPixelSizeLB = PadlockButton(self)
        self._yPixelSizeLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._yPixelSizeLB)
        self._tree.setItemWidget(self._yPixelSizeQTWI, 2, self._yPixelSizeLB)

        ## distance
        self._sampleDetectorDistanceQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._sampleDetectorDistanceQTWI.setText(0, "distance")
        self._distanceMetricEntry = MetricEntry("", parent=self)
        self._distanceMetricEntry.layout().setContentsMargins(2, 2, 2, 2)
        self._tree.setItemWidget(
            self._sampleDetectorDistanceQTWI, 1, self._distanceMetricEntry
        )
        self._editableWidgets.append(self._distanceMetricEntry)
        self._distanceLB = PadlockButton(self)
        self._distanceLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._distanceLB)
        self._tree.setItemWidget(self._sampleDetectorDistanceQTWI, 2, self._distanceLB)

        ## field of view
        self._fieldOfViewQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._fieldOfViewQTWI.setText(0, "field of view")
        self._fieldOfViewCB = qt.QComboBox(self)
        for value in FOV.values():
            self._fieldOfViewCB.addItem(value)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 1, self._fieldOfViewCB)
        self._editableWidgets.append(self._fieldOfViewCB)
        self._fieldOfViewLB = PadlockButton(self)
        self._fieldOfViewLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._fieldOfViewLB)
        self._tree.setItemWidget(self._fieldOfViewQTWI, 2, self._fieldOfViewLB)

        ## x flipped
        self._xFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._xFlippedQTWI.setText(0, "x flipped")
        self._xFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._xFlippedQTWI, 1, self._xFlippedCB)
        self._editableWidgets.append(self._xFlippedCB)
        self._xFlippedLB = PadlockButton(self)
        self._xFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._xFlippedLB)
        self._tree.setItemWidget(self._xFlippedQTWI, 2, self._xFlippedLB)
        ## y flipped
        self._yFlippedQTWI = qt.QTreeWidgetItem(self._detectorQTWI)
        self._yFlippedQTWI.setText(0, "y flipped")
        self._yFlippedCB = qt.QCheckBox("", self)
        self._tree.setItemWidget(self._yFlippedQTWI, 1, self._yFlippedCB)
        self._editableWidgets.append(self._yFlippedCB)
        self._yFlippedLB = PadlockButton(self)
        self._yFlippedLB.setMaximumSize(30, 30)
        self._lockerPBs.append(self._yFlippedLB)
        self._tree.setItemWidget(self._yFlippedQTWI, 2, self._yFlippedLB)
        # 2: sample
        self._sampleQTWI = qt.QTreeWidgetItem(self._tree)
        self._sampleQTWI.setText(0, "sample")
        ## x translation
        self._xTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._xTranslationQTWI.setText(0, "x translation")
        self._xTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._xTranslationQTWI, 1, self._xTranslationQLE)
        self._editableWidgets.append(self._xTranslationQLE)

        ## z translation
        self._zTranslationQTWI = qt.QTreeWidgetItem(self._sampleQTWI)
        self._zTranslationQTWI.setText(0, "z translation")
        self._zTranslationQLE = _TranslationMetricEntry(name="", parent=self)
        self._tree.setItemWidget(self._zTranslationQTWI, 1, self._zTranslationQLE)
        self._editableWidgets.append(self._zTranslationQLE)

        # set up
        self._instrumentQTWI.setExpanded(True)
        self._sampleQTWI.setExpanded(True)
        self._beamQTWI.setExpanded(True)
        self._detectorQTWI.setExpanded(True)
        self.hideLockers(hide_lockers)

        # connect signal / slot
        self._energyEntry.editingFinished.connect(self._editingFinished)
        self._energyLockerLB.toggled.connect(self._editingFinished)
        self._xPixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._xPixelSizeLB.toggled.connect(self._editingFinished)
        self._yPixelSizeMetricEntry.editingFinished.connect(self._editingFinished)
        self._yPixelSizeLB.toggled.connect(self._editingFinished)
        self._distanceMetricEntry.editingFinished.connect(self._editingFinished)
        self._distanceLB.toggled.connect(self._editingFinished)
        self._fieldOfViewCB.currentIndexChanged.connect(self._editingFinished)
        self._fieldOfViewLB.toggled.connect(self._editingFinished)
        self._xFlippedCB.toggled.connect(self._editingFinished)
        self._xFlippedLB.toggled.connect(self._editingFinished)
        self._yFlippedCB.toggled.connect(self._editingFinished)
        self._yFlippedLB.toggled.connect(self._editingFinished)

    def update_tree(self) -> None:
        if self.getScan() is not None:
            self._updateInstrument()
            self._updateSample()
            self._tree.resizeColumnToContents(0)

    def _updateInstrument(self) -> None:
        scan = self.getScan()
        if scan is None:
            return
        else:
            for name, fct in {
                "energy": self._updateEnergy,
                "pixel size": self._updatePixelSize,
                "frame flips": self._updateFlipped,
                "field of view": self._updateFieldOfView,
                "sample-detector distance": self._updateDistance,
            }.items():
                try:
                    fct(scan=scan)
                except Exception as e:
                    _logger.error(f"Failed to update {name}. Error is {e}")

    def _updateSample(self) -> None:
        scan = self.getScan()
        if scan is None:
            return
        else:
            try:
                self._updateTranslations(scan=scan)
            except Exception as e:
                _logger.error(f"Fail to update translations. Error is {e}")

    def _updateTranslations(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)

        # note: for now and in order to allow edition we expect to have at most a unique value. Will fail for helicoidal
        def reduce(values):
            if values is None:
                return None
            values = numpy.array(values)
            values = numpy.unique(
                values[scan.image_key_control == ImageKey.PROJECTION.value]
            )
            if values.size == 1:
                return values[0]
            elif values.size == 0:
                return None
            else:
                return f"{values[0]} ... {values[-1]}"

        x_translation = reduce(scan.x_translation)
        z_translation = reduce(scan.z_translation)
        self._xTranslationQLE.setValue(x_translation)
        self._zTranslationQLE.setValue(z_translation)

    def _updateFieldOfView(self, scan: NXtomoScan) -> None:
        if not self._fieldOfViewLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            idx = self._fieldOfViewCB.findText(FOV.from_value(scan.field_of_view).value)
            if idx > 0:
                self._fieldOfViewCB.setCurrentIndex(idx)

    def _updateFlipped(self, scan: NXtomoScan) -> None:
        transformations = list(scan.get_detector_transformations(tuple()))
        transformation_matrix_det_space = build_matrix(transformations)
        if transformation_matrix_det_space is None or numpy.allclose(
            transformation_matrix_det_space, numpy.identity(3)
        ):
            flip_ud = False
            flip_lr = False
        elif numpy.array_equal(
            transformation_matrix_det_space, NXtomoEditorTask.Y_FLIP_MATRIX
        ):
            flip_ud = True
            flip_lr = False
        elif numpy.allclose(
            transformation_matrix_det_space, NXtomoEditorTask.Z_FLIP_MATRIX
        ):
            flip_ud = False
            flip_lr = True
        elif numpy.allclose(
            transformation_matrix_det_space, NXtomoEditorTask.Y_AND_Z_flip_MATRIX
        ):
            flip_ud = True
            flip_lr = True
        else:
            flip_ud = None
            flip_lr = None
            _logger.warning(
                "detector transformations provided not handled... For now only handle up-down flip as left-right flip"
            )
        if (not self._xFlippedLB.isLocked()) and flip_lr is not None:
            self._xFlippedCB.setChecked(flip_lr)
        if (not self._yFlippedLB.isLocked()) and flip_ud is not None:
            self._yFlippedCB.setChecked(flip_ud)

    def _updateDistance(self, scan: NXtomoScan) -> None:
        if not self._distanceLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            self._distanceMetricEntry.setValue(scan.distance)

    def _updateEnergy(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)
        if not self._energyLockerLB.isLocked():
            # if in ''auto mode: we want to overwrite the NXtomo existing value by the one of the GUI
            energy = scan.energy
            self._energyEntry.setValue(energy)

    def _updatePixelSize(self, scan: NXtomoScan) -> None:
        assert isinstance(scan, NXtomoScan)
        if not self._xPixelSizeLB.isLocked():
            x_pixel_size = scan.x_pixel_size
            self._xPixelSizeMetricEntry.setValue(x_pixel_size)
        if not self._yPixelSizeLB.isLocked():
            y_pixel_size = scan.y_pixel_size
            self._yPixelSizeMetricEntry.setValue(y_pixel_size)

    def _editingFinished(self, *args, **kwargs):
        self.sigEditingFinished.emit()

    def hasLockField(self) -> bool:
        """return True if the widget has at least one lock field"""
        return True in [locker.isLocked() for locker in self._lockerPBs]

    def hideLockers(self, hide: bool) -> None:
        for locker in self._lockerPBs:
            locker.setVisible(not hide)

    def getEditableWidgets(self) -> tuple[qt.QWidget]:
        return tuple(self._editableWidgets)

    def setScan(self, scan: NXtomoScan | None) -> None:
        if scan is None:
            self._scan = scan
        elif not isinstance(scan, NXtomoScan):
            raise TypeError(
                f"{scan} is expected to be an instance of {NXtomoScan}. Not {type(scan)}"
            )
        else:
            self._scan = weakref.ref(scan)
        self._scanInfoQLE.setScan(scan)
        # scan will only be read and not kept
        self.update_tree()

    def getScan(self) -> NXtomoScan | None:
        if self._scan is None or self._scan() is None:
            return None
        else:
            return self._scan()

    def getConfiguration(self) -> dict:
        """
        Return a dict with field full name as key
        and a tuple as value (field_value, is_locked)

        limitation: for now sample position are not handled because this is a 'corner case' for now
        """
        return {
            NXtomoEditorKeys.ENERGY: (
                self._energyEntry.getValue(),
                self._energyLockerLB.isLocked(),
            ),
            NXtomoEditorKeys.X_PIXEL_SIZE: (
                self._xPixelSizeMetricEntry.getValue(),
                self._xPixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.Y_PIXEL_SIZE: (
                self._yPixelSizeMetricEntry.getValue(),
                self._yPixelSizeLB.isLocked(),
            ),
            NXtomoEditorKeys.SAMPLE_DETECTOR_DISTANCE: (
                self._distanceMetricEntry.getValue(),
                self._distanceLB.isLocked(),
            ),
            NXtomoEditorKeys.FIELD_OF_VIEW: (
                self._fieldOfViewCB.currentText(),
                self._fieldOfViewLB.isChecked(),
            ),
            NXtomoEditorKeys.X_FLIPPED: (
                self._xFlippedCB.isChecked(),
                self._xFlippedLB.isChecked(),
            ),
            NXtomoEditorKeys.Y_FLIPPED: (
                self._yFlippedCB.isChecked(),
                self._yFlippedLB.isChecked(),
            ),
            NXtomoEditorKeys.X_TRANSLATION: (self._xTranslationQLE.getValue(),),
            NXtomoEditorKeys.Z_TRANSLATION: (self._zTranslationQLE.getValue(),),
        }

    def setConfiguration(self, config: dict) -> None:
        energy = config.get("instrument.beam.energy", None)
        if energy is not None:
            energy, energy_locked = energy
            self._energyEntry.setValue(energy)
            self._energyLockerLB.setLock(energy_locked)

        x_pixel_size = config.get("instrument.detector.x_pixel_size", None)
        if x_pixel_size is not None:
            x_pixel_size, x_pixel_size_locked = x_pixel_size
            self._xPixelSizeMetricEntry.setValue(x_pixel_size)
            self._xPixelSizeLB.setLock(x_pixel_size_locked)

        y_pixel_size = config.get("instrument.detector.y_pixel_size", None)
        if y_pixel_size is not None:
            y_pixel_size, y_pixel_size_locked = y_pixel_size
            self._yPixelSizeMetricEntry.setValue(y_pixel_size)
            self._yPixelSizeLB.setLock(y_pixel_size_locked)

        detector_sample_distance = config.get("instrument.detector.distance", None)
        if detector_sample_distance is not None:
            detector_sample_distance, distance_locked = detector_sample_distance
            self._distanceMetricEntry.setValue(detector_sample_distance)
            self._distanceLB.setLock(x_pixel_size_locked)

        field_of_view = config.get("instrument.detector.field_of_view", None)
        if field_of_view is not None:
            field_of_view, field_of_view_locked = field_of_view
            self._fieldOfViewCB.setCurrentText(field_of_view)
            self._fieldOfViewLB.setLock(field_of_view_locked)

        x_flipped = config.get("instrument.detector.x_flipped", None)
        if x_flipped is not None:
            x_flipped, x_flipped_locked = x_flipped
            x_flipped = x_flipped in (True, "True", "true")
            self._xFlippedCB.setChecked(x_flipped)
            self._xFlippedLB.setLock(x_flipped_locked)

        y_flipped = config.get("instrument.detector.y_flipped", None)
        if y_flipped is not None:
            y_flipped, y_flipped_locked = y_flipped
            y_flipped = y_flipped in (True, "True", "true")
            self._yFlippedCB.setChecked(y_flipped)
            self._yFlippedLB.setLock(y_flipped_locked)

    def getConfigurationForTask(self) -> dict:
        """
        default configuration is stored as field: (field_value, filed_is_locked) when the task expects field_key: field_value
        Because we need to be able to reload settings of the LockButton.
        But the task doesn't care about it. She only want to know which field must be edited. So we need to filter the dict value.
        """
        return {key: value[0] for key, value in self.getConfiguration().items()}

    def clear(self) -> None:
        self._tree.clear()


class _TranslationMetricEntry(MetricEntry):
    """
    Widget to define a translation along one axis.

    The behavior is limited at the moment.
    * either the array contains a unique value on the array and a float is displayed
    * either the array contains several unique values and then '...' will be displayed. Users cannot provide an array in this case.
    """

    LOADED_ARRAY = "loaded array"

    class TranslationValidator(qt.QDoubleValidator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setNotation(qt.QDoubleValidator.ScientificNotation)

        def validate(self, a0: str, a1: int):
            if "..." in a0:
                return (qt.QDoubleValidator.Acceptable, a0, a1)
            else:
                return super().validate(a0, a1)

    def __init__(self, name, default_unit="m", parent=None):
        super().__init__(name, default_unit=default_unit, parent=parent)
        self._qlePixelSize.setValidator(self.TranslationValidator(self))

    def getValue(self) -> float:
        """

        :return: the value in meter
        """
        if "..." in self._qlePixelSize.text():
            # in this case this is the representation of an array, we don;t wan't to overwrite it
            return self.LOADED_ARRAY
        if self._qlePixelSize.text() in ("unknown", ""):
            return None
        else:
            return float(self._qlePixelSize.text()) * self.getCurrentUnit()


class EnergyEntry(qt.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setValidator(MetricEntry.DoubleValidator())

    def setValue(self, a0):
        if a0 is None:
            a0 = "unknown"
        else:
            a0 = str(a0)
        super().setText(a0)

    def getValue(self) -> float | None:
        txt = self.text().replace(" ", "")
        if txt in ("unknown", ""):
            return None
        else:
            return float(txt)
