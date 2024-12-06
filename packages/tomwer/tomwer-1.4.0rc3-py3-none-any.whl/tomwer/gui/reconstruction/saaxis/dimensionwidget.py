"""
contains gui relative to semi-automatic axis calculation
"""

from __future__ import annotations

from typing import Iterable

from silx.gui import qt
from pyunitsystem.metricsystem import MetricSystem
from tomwer.gui.utils.qt_utils import block_signals


class DimensionWidget(qt.QGroupBox):
    """
    Simple widget to display value over 3 dimensions

    :param parent:
    :param title: QGroupBox title
    :param dims_name: name of the dimension. If set will be store in each
                      QDoubleLine prefix
    :param dims_colors: color associated to the three dimensions if any
    """

    valuesChanged = qt.Signal()
    """Signal emitted when a value change"""

    def __init__(
        self, parent=None, title=None, dims_name=None, dims_colors=None, title_size=10
    ):
        qt.QGroupBox.__init__(self, parent)
        self.setFont(qt.QFont("Arial", title_size))
        assert title is not None
        assert dims_name is None or (
            isinstance(dims_name, Iterable) and len(dims_name) == 3
        )
        assert dims_colors is None or (
            isinstance(dims_colors, Iterable) and len(dims_colors) == 3
        )
        self._dim0Value = 1.0 * MetricSystem.MILLIMETER.value
        self._dim1Value = 1.0 * MetricSystem.MILLIMETER.value
        self._dim2Value = 1.0 * MetricSystem.MILLIMETER.value
        self._displayUnit = MetricSystem.MILLIMETER
        # defined unit to display values. Always stored in m (International
        # System)
        ## set GUI
        self.setTitle(title)
        self.setLayout(qt.QHBoxLayout())
        # dim 0
        self._dim0ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim0ValueQLE.setPrefix(dims_name[0])
        self._dim0ValueQLE.setRange(0, 999999999999)
        self._dim0ValueQLE.setDecimals(10)
        self._dim0ValueQLE.setSingleStep(0.0001)
        self._dim0ValueQLE.setValue(self._getDim0DisplayValue())
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[0]}"
            self._dim0ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim0ValueQLE)
        # dim 1
        self._dim1ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim1ValueQLE.setPrefix(dims_name[1])
        self._dim1ValueQLE.setRange(0, 999999999999)
        self._dim1ValueQLE.setDecimals(10)
        self._dim1ValueQLE.setSingleStep(0.0001)
        self._dim1ValueQLE.setValue(self._getDim1DisplayValue())
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[1]}"
            self._dim1ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim1ValueQLE)
        # dim 2
        self._dim2ValueQLE = qt.QDoubleSpinBox(self)
        if dims_name is not None:
            self._dim2ValueQLE.setPrefix(dims_name[2])
        self._dim2ValueQLE.setRange(0, 999999999999)
        self._dim2ValueQLE.setDecimals(10)
        self._dim2ValueQLE.setSingleStep(0.0001)
        self._dim2ValueQLE.setValue(self._getDim2DisplayValue())
        if dims_colors is not None:
            stylesheet = f"background-color: {dims_colors[2]}"
            self._dim2ValueQLE.setStyleSheet(stylesheet)
        self.layout().addWidget(self._dim2ValueQLE)

        # set up
        self.setUnit(self._displayUnit)

        # connect signal / slot
        self._dim0ValueQLE.editingFinished.connect(self._userSetDim0)
        self._dim1ValueQLE.editingFinished.connect(self._userSetDim1)
        self._dim2ValueQLE.editingFinished.connect(self._userSetDim2)

    def _getDim0DisplayValue(self) -> float:
        return self._dim0Value / self._displayUnit.value

    def _getDim1DisplayValue(self) -> float:
        return self._dim1Value / self._displayUnit.value

    def _getDim2DisplayValue(self) -> float:
        return self._dim2Value / self._displayUnit.value

    def setUnit(self, unit):
        """
        define with which unit we should display the size
        :param unit: metric to be used for display. Internally this is always stored using the international metric system
        """
        self._displayUnit = MetricSystem.from_value(unit)
        for widget in (self._dim0ValueQLE, self._dim1ValueQLE, self._dim2ValueQLE):
            widget.setSuffix(str(self.unit()))
        # update displayed values
        with block_signals(self):
            self._dim0ValueQLE.setValue(self._getDim0DisplayValue())
            self._dim1ValueQLE.setValue(self._getDim1DisplayValue())
            self._dim2ValueQLE.setValue(self._getDim2DisplayValue())

    def unit(self) -> MetricSystem:
        """

        :return: metric system used for display
        """
        return self._displayUnit

    def setValues(
        self,
        dim0: float,
        dim1: float,
        dim2: float,
        unit: str | MetricSystem = "mm",
    ) -> None:
        """

        :param dim0: value to dim0
        :param dim1: value to dim1
        :param dim2: value to dim2
        :param unit: unit used for the provided values
        """
        with block_signals(self):
            self.setDim0value(value=dim0, unit=unit)
            self.setDim1value(value=dim1, unit=unit)
            self.setDim2value(value=dim2, unit=unit)
        self.valuesChanged.emit()

    def getValues(self) -> tuple:
        """

        :return: (dim0 value, dim1 value, dim2 value, unit)
        """
        return (
            self.getDim0Value()[0],
            self.getDim1Value()[0],
            self.getDim2Value()[0],
            MetricSystem.METER,
        )

    def getDim0Value(self) -> tuple:
        """Return Dim 0 value and unit. Unit is always meter"""
        return self._dim0Value, MetricSystem.METER

    def setDim0value(self, value: str | MetricSystem, unit="mm"):
        """

        :param value: value to set to dim 0.
        :return:
        """
        self._dim0Value = value * MetricSystem.from_value(unit).value
        with block_signals(self):
            self._dim0ValueQLE.setValue(self._dim0Value)
        self.valuesChanged.emit()

    def getDim1Value(self) -> tuple:
        """Return Dim 0 value and unit. Unit is always meter"""
        return self._dim1Value, MetricSystem.METER

    def setDim1value(self, value: str | MetricSystem, unit="mm"):
        """

        :param value: value to set to dim 1.
        :return:
        """
        self._dim1Value = value * MetricSystem.from_value(unit).value
        with block_signals(self):
            self._dim1ValueQLE.setValue(self._dim1Value)
        self.valuesChanged.emit()

    def getDim2Value(self) -> tuple:
        """Return Dim 0 value and unit. Unit is always meter"""
        return self._dim2Value, MetricSystem.METER

    def setDim2value(self, value: str | MetricSystem, unit="mm"):
        """

        :param value: value to set to dim 2.
        :return:
        """
        self._dim2Value = value * MetricSystem.from_value(unit).value
        with block_signals(self):
            self._dim2ValueQLE.setValue(self._dim2Value)
        self.valuesChanged.emit()

    def _valuesChanged(self, *args, **kwargs):
        self.valuesChanged.emit()

    def _userSetDim0(self):
        """callback when the user modify the dim 0 QDSP"""
        with block_signals(self):
            self._dim0Value = self._dim0ValueQLE.value() * self.unit().value
        self.valuesChanged.emit()

    def _userSetDim1(self):
        """callback when the user modify the dim 1 QDSP"""
        with block_signals(self):
            self._dim1Value = self._dim1ValueQLE.value() * self.unit().value
        self.valuesChanged.emit()

    def _userSetDim2(self):
        """callback when the user modify the dim 2 QDSP"""
        with block_signals(self):
            self._dim2Value = self._dim2ValueQLE.value() * self.unit().value
        self.valuesChanged.emit()
