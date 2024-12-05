# coding: utf-8

"""
This module is used to define the process of the reference creator.
This is related to the issue #184
"""

from __future__ import annotations


import logging

from silx.gui import qt
from pyunitsystem.metricsystem import MetricSystem

from tomwer.core.utils.char import MU_CHAR

_logger = logging.getLogger(__name__)


class PixelEntry(qt.QWidget):
    valueChanged = qt.Signal()
    """emit when the pixel value change"""

    class Validator(qt.QIntValidator):
        def validate(self, a0: str, a1: int):
            if a0 == "unknow":
                return qt.QValidator.Acceptable
            else:
                return super().validate(a0, a1)

    def __init__(self, name, parent=None):
        qt.QWidget.__init__(self, parent)

        self.setLayout(qt.QHBoxLayout())
        self._label = qt.QLabel(name, parent=self)
        self.layout().addWidget(self._label)
        self._qlePixelSize = qt.QLineEdit(parent=self)
        self._qlePixelSize.setValidator(self.Validator(self._qlePixelSize))
        self._qlePixelSize.setPlaceholderText("px")
        self.layout().addWidget(self._qlePixelSize)

        # connect signal / slot
        self._qlePixelSize.editingFinished.connect(self.valueChanged)

    def getValue(self):
        if self._qlePixelSize.text() in ("unknown", ""):
            return None
        else:
            return int(self._qlePixelSize.text())

    def setValue(self, value: int):
        self._qlePixelSize.setText(str(value))
        self.valueChanged.emit()

    def setReadOnly(self, read_only: bool) -> None:
        self._qlePixelSize.setReadOnly(read_only)


class MetricEntry(qt.QWidget):
    """
    Create a simple line with a name, a QLineEdit and a combobox to define the
    unit in order to define a metric value.

    :param name: name of the metric value to define
    :param default_unit: Default way to present a value when set
    """

    editingFinished = qt.Signal()
    """emit when editing is finished"""

    class DoubleValidator(qt.QDoubleValidator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.setNotation(qt.QDoubleValidator.ScientificNotation)

        def validate(self, a0: str, a1: int):
            if a0 == "unknown":
                return (qt.QDoubleValidator.Acceptable, a0, a1)
            else:
                return super().validate(a0, a1)

    _CONVERSION = {
        "nm": MetricSystem.NANOMETER.value,
        f"{MU_CHAR}m": MetricSystem.MICROMETER.value,
        "mm": MetricSystem.MILLIMETER.value,
        "cm": MetricSystem.CENTIMETER.value,
        "m": MetricSystem.METER.value,
    }

    valueChanged = qt.Signal()
    """emit when the metric value change"""

    def __init__(self, name, value=0.0, default_unit="m", parent=None):
        qt.QWidget.__init__(self, parent)
        assert type(default_unit) is str
        assert default_unit in ("nm", "mm", "cm", "m", f"{MU_CHAR}m")
        self._base_unit = default_unit

        self.setLayout(qt.QHBoxLayout())
        self._label = qt.QLabel(name, parent=self)
        self.layout().addWidget(self._label)
        self._qlePixelSize = qt.QLineEdit("0.0", parent=self)
        self._qlePixelSize.setValidator(self.DoubleValidator(self._qlePixelSize))
        self.layout().addWidget(self._qlePixelSize)

        self._qcbUnit = qt.QComboBox(parent=self)
        self._qcbUnit.addItem("nm")
        self._qcbUnit.addItem(f"{MU_CHAR}m")
        self._qcbUnit.addItem("mm")
        self._qcbUnit.addItem("cm")
        self._qcbUnit.addItem("m")
        self.layout().addWidget(self._qcbUnit)
        self._resetBaseUnit()

        # connect signal / slot
        self._qcbUnit.currentIndexChanged.connect(self._editingFinished)
        self._qlePixelSize.editingFinished.connect(self._editingFinished)

    def _editingFinished(self, *args, **kwargs):
        self.editingFinished.emit()

    def setReadOnly(self, a0: bool):
        self._qlePixelSize.setReadOnly(a0)
        self._qcbUnit.setEnabled(not a0)

    def setLabelText(self, text: str):
        self._label.setText(text)

    def getCurrentUnit(self):
        assert self._qcbUnit.currentText() in self._CONVERSION
        return self._CONVERSION[self._qcbUnit.currentText()]

    def setValue(self, value_m, displayed_unit: str = "m"):
        """

        :param value: pixel size in international metric system (meter)
        """
        _value = value_m
        if _value in (None, "unknown"):
            txt = "unknown"
        elif isinstance(_value, str):
            if "..." in _value:
                txt = _value
            else:
                try:
                    _value = float(_value)
                except Exception as error:
                    raise ValueError("Given string does not represent a float", error)
                else:
                    assert isinstance(_value, float)
                    txt = str(_value)
        else:
            txt = str(_value)
        self._qlePixelSize.setText(txt)
        self._resetBaseUnit(displayed_unit=displayed_unit)

    def _resetBaseUnit(self, displayed_unit=None):
        """Simple reset of the combobox according to the base_unit"""
        displayed_unit = displayed_unit or self._base_unit
        index = self._qcbUnit.findText(displayed_unit)
        if index is None:
            raise ValueError("unrecognized base unit")
        else:
            self._qcbUnit.setCurrentIndex(index)

    def getValue(self) -> float:
        """

        :return: the value in meter
        """
        if self._qlePixelSize.text() in ("unknown", ""):
            return None
        else:
            return float(self._qlePixelSize.text()) * self.getCurrentUnit()

    def setValidator(self, validator):
        self._qlePixelSize.setValidator(validator)

    def setUnit(self, unit):
        unit = str(MetricSystem.from_value(unit))
        idx = self._qcbUnit.findText(unit)
        self._qcbUnit.setCurrentIndex(idx)
