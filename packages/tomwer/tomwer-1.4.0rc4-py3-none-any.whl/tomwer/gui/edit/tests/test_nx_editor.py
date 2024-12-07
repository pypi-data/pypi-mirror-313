import os
import h5py

import numpy
import pytest
from silx.gui import qt

from pyunitsystem.energysystem import EnergySI
from pyunitsystem.metricsystem import MetricSystem

from nxtomo.application.nxtomo import NXtomo
from nxtomo.nxobject.nxdetector import ImageKey, FOV
from nxtomo.utils.transformation import (
    build_matrix,
    DetYFlipTransformation,
    DetZFlipTransformation,
)
from nxtomo.nxobject.nxtransformations import NXtransformations

from tomwer.core.process.edit.nxtomoeditor import NXtomoEditorTask
from tomwer.core.scan.nxtomoscan import NXtomoScan
from tomwer.gui.edit.nxtomoeditor import NXtomoEditor, _TranslationMetricEntry
from tomwer.tests.conftest import qtapp  # noqa F401


@pytest.mark.parametrize("x_pixel_size", (None, 0.12))
@pytest.mark.parametrize("y_pixel_size", (None, 0.0065))
@pytest.mark.parametrize("field_of_view", FOV.values())
@pytest.mark.parametrize("distance", (None, 1.2))
@pytest.mark.parametrize("energy", (None, 23.5))
@pytest.mark.parametrize("x_flipped", (True, False))
@pytest.mark.parametrize("y_flipped", (True, False))
@pytest.mark.parametrize("x_translation", (None, numpy.ones(12), numpy.arange(12)))
@pytest.mark.parametrize("z_translation", (None, numpy.zeros(12), numpy.arange(12, 24)))
def test_nx_editor(
    tmp_path,
    qtapp,  # noqa F811
    x_pixel_size,
    y_pixel_size,
    field_of_view,
    distance,
    energy,
    x_flipped,
    y_flipped,
    x_translation,
    z_translation,
):
    # 1.0 create nx tomo with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.x_pixel_size = x_pixel_size
    nx_tomo.instrument.detector.y_pixel_size = y_pixel_size
    nx_tomo.instrument.detector.field_of_view = field_of_view
    nx_tomo.instrument.detector.distance = distance
    nx_tomo.energy = energy
    nx_tomo.sample.x_translation = x_translation
    nx_tomo.sample.z_translation = z_translation
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12)

    nx_tomo.instrument.detector.transformations.add_transformation(
        DetZFlipTransformation(flip=x_flipped)
    )
    nx_tomo.instrument.detector.transformations.add_transformation(
        DetYFlipTransformation(flip=y_flipped)
    )

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )

    scan = NXtomoScan(file_path, entry)

    # 2.0 create the widget and do the edition
    widget = NXtomoEditor()
    widget.setScan(scan=scan)

    # 3.0 check data have been correctly loaded
    def check_metric(expected_value, current_value):
        if expected_value is None:
            return current_value is None
        return numpy.isclose(expected_value, float(current_value))

    assert check_metric(x_pixel_size, widget._xPixelSizeMetricEntry.getValue())
    assert widget._xPixelSizeMetricEntry._qcbUnit.currentText() == "m"
    assert check_metric(y_pixel_size, widget._yPixelSizeMetricEntry.getValue())
    assert widget._yPixelSizeMetricEntry._qcbUnit.currentText() == "m"

    assert check_metric(distance, widget._distanceMetricEntry.getValue())
    assert widget._distanceMetricEntry._qcbUnit.currentText() == "m"

    assert field_of_view == widget._fieldOfViewCB.currentText()
    assert x_flipped == widget._xFlippedCB.isChecked()
    assert y_flipped == widget._yFlippedCB.isChecked()

    if energy is None:
        assert widget._energyEntry.getValue() is None
    else:
        assert numpy.isclose(energy, widget._energyEntry.getValue())

    def check_translation(expected_value, current_value):
        if expected_value is None:
            return current_value is None
        else:
            u_values = numpy.unique(expected_value)
            if u_values.size == 1:
                return float(current_value) == u_values[0]
            else:
                return current_value is _TranslationMetricEntry.LOADED_ARRAY

    assert check_translation(x_translation, widget._xTranslationQLE.getValue())
    assert widget._xTranslationQLE._qcbUnit.currentText() == "m"
    assert check_translation(z_translation, widget._zTranslationQLE.getValue())
    assert widget._zTranslationQLE._qcbUnit.currentText() == "m"

    # 4.0 edit some parameters
    widget._energyEntry.setText("23.789")
    widget._xPixelSizeMetricEntry.setUnit("nm")
    widget._yPixelSizeMetricEntry.setValue(2.1e-7)
    widget._distanceMetricEntry.setValue("unknown")
    widget._fieldOfViewCB.setCurrentText(FOV.HALF.value)
    widget._xFlippedCB.setChecked(not x_flipped)
    widget._xTranslationQLE.setValue(1.8)
    widget._xTranslationQLE.setUnit("mm")
    widget._zTranslationQLE.setValue(2.8)
    widget._zTranslationQLE.setUnit("m")

    # 5.0
    task = NXtomoEditorTask(
        inputs={
            "data": scan,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # 6.0 make sure data have been overwrite
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )

    assert overwrite_nx_tomo.energy.value == 23.789
    assert overwrite_nx_tomo.energy.unit == EnergySI.KILOELECTRONVOLT

    if x_pixel_size is None:
        assert overwrite_nx_tomo.instrument.detector.x_pixel_size.value is None
    else:
        assert numpy.isclose(
            overwrite_nx_tomo.instrument.detector.x_pixel_size.si_value,
            x_pixel_size * MetricSystem.NANOMETER.value,
        )
    assert overwrite_nx_tomo.instrument.detector.y_pixel_size.si_value == 2.1e-7

    assert overwrite_nx_tomo.instrument.detector.distance.value is None
    assert overwrite_nx_tomo.instrument.detector.field_of_view is FOV.HALF

    final_transformation = NXtransformations()

    final_transformation.add_transformation(DetYFlipTransformation(flip=y_flipped))
    final_transformation.add_transformation(DetZFlipTransformation(flip=not x_flipped))
    # note: the 'not' comes from inversion done with the _xFlippedCB combobox

    numpy.testing.assert_allclose(
        build_matrix(
            overwrite_nx_tomo.instrument.detector.transformations.transformations
        ),
        build_matrix(final_transformation.transformations),
    )

    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.sample.x_translation.si_value,
        numpy.array([1.8 * MetricSystem.MILLIMETER.value] * 12),
    )
    assert overwrite_nx_tomo.sample.x_translation.unit is MetricSystem.METER
    numpy.testing.assert_array_almost_equal(
        overwrite_nx_tomo.sample.z_translation.si_value,
        numpy.array([2.8 * MetricSystem.METER.value] * 12),
    )
    assert overwrite_nx_tomo.sample.z_translation.unit is MetricSystem.METER
    # end
    widget.setAttribute(qt.Qt.WA_DeleteOnClose)
    widget.close()
    widget = None


def test_nx_editor_lock(
    tmp_path,
    qtapp,  # noqa F811
):
    """test the pad lock buttons of the NXtomo editor"""
    # 1.0 create nx tomos with raw data
    nx_tomo_1 = NXtomo()
    nx_tomo_1.instrument.detector.x_pixel_size = 0.023
    nx_tomo_1.instrument.detector.y_pixel_size = 0.025
    nx_tomo_1.instrument.detector.field_of_view = "full"
    nx_tomo_1.instrument.detector.distance = 2.4
    nx_tomo_1.instrument.detector.x_flipped = False
    nx_tomo_1.instrument.detector.y_flipped = True
    nx_tomo_1.energy = 5.9
    nx_tomo_1.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo_1.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo_1.sample.rotation_angle = numpy.linspace(0, 20, num=12)

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo_1.save(
        file_path=file_path,
        data_path=entry,
    )

    scan_1 = NXtomoScan(file_path, entry)

    nx_tomo_2 = NXtomo()
    nx_tomo_2.instrument.detector.x_pixel_size = 4.023
    nx_tomo_2.instrument.detector.y_pixel_size = 6.025
    nx_tomo_2.instrument.detector.field_of_view = "full"
    nx_tomo_2.instrument.detector.distance = 2.89
    nx_tomo_2.instrument.detector.x_flipped = (
        not nx_tomo_1.instrument.detector.x_flipped
    )
    nx_tomo_2.instrument.detector.y_flipped = (
        not nx_tomo_1.instrument.detector.y_flipped
    )
    nx_tomo_2.energy = 5.754
    nx_tomo_2.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo_2.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo_2.sample.rotation_angle = numpy.linspace(0, 20, num=12)

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0001"
    nx_tomo_2.save(
        file_path=file_path,
        data_path=entry,
    )

    scan_2 = NXtomoScan(file_path, entry)

    # 2.0 create the widget and do the edition
    widget = NXtomoEditor()
    widget.setScan(scan=scan_1)

    for lockerButton in widget._lockerPBs:
        lockerButton.setLock(True)

    widget.setScan(scan=scan_2)
    # widget values must be the same (NXtomo field value not loaded if the lockers are active)
    assert widget._energyEntry.getValue() == 5.9
    assert widget._xPixelSizeMetricEntry.getValue() == 0.023
    assert widget._yPixelSizeMetricEntry.getValue() == 0.025
    assert widget._distanceMetricEntry.getValue() == 2.4
    assert widget._fieldOfViewCB.currentText() == "Full"
    assert not widget._xFlippedCB.isChecked()
    assert widget._yFlippedCB.isChecked()

    # 3.0 save the nxtomo
    task = NXtomoEditorTask(
        inputs={
            "data": scan_2,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # 4.0 check save went well
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )
    assert (
        overwrite_nx_tomo.instrument.detector.x_pixel_size.value
        == nx_tomo_1.instrument.detector.x_pixel_size.value
    )
    assert (
        overwrite_nx_tomo.instrument.detector.y_pixel_size.value
        == nx_tomo_1.instrument.detector.y_pixel_size.value
    )
    assert (
        overwrite_nx_tomo.instrument.detector.field_of_view
        == nx_tomo_1.instrument.detector.field_of_view
    )
    assert (
        overwrite_nx_tomo.instrument.detector.distance.value
        == nx_tomo_1.instrument.detector.distance.value
    )
    assert (
        overwrite_nx_tomo.instrument.detector.x_flipped
        == nx_tomo_1.instrument.detector.x_flipped
    )
    assert (
        overwrite_nx_tomo.instrument.detector.y_flipped
        == nx_tomo_1.instrument.detector.y_flipped
    )
    assert overwrite_nx_tomo.energy.value == nx_tomo_1.energy.value

    assert widget.getConfiguration() == {
        "instrument.beam.energy": (5.9, True),
        "instrument.detector.distance": (2.4, True),
        "instrument.detector.field_of_view": ("Full", True),
        "instrument.detector.x_pixel_size": (0.023, True),
        "instrument.detector.y_pixel_size": (0.025, True),
        "instrument.detector.x_flipped": (False, True),
        "instrument.detector.y_flipped": (True, True),
        "sample.x_translation": (None,),
        "sample.z_translation": (None,),
    }

    for lockerButton in widget._lockerPBs:
        lockerButton.setLock(False)

    assert widget.getConfiguration() == {
        "instrument.beam.energy": (5.9, False),
        "instrument.detector.distance": (2.4, False),
        "instrument.detector.field_of_view": ("Full", False),
        "instrument.detector.x_pixel_size": (0.023, False),
        "instrument.detector.y_pixel_size": (0.025, False),
        "instrument.detector.x_flipped": (False, False),
        "instrument.detector.y_flipped": (True, False),
        "sample.x_translation": (None,),
        "sample.z_translation": (None,),
    }


def test_nxtomo_editor_with_missing_paths(
    tmp_path,
    qtapp,  # noqa F811
):
    """
    test widget behavior in the case some nxtomo path don't exist
    """

    # create nx tomo with raw data
    nx_tomo = NXtomo()
    nx_tomo.instrument.detector.image_key_control = [ImageKey.PROJECTION.value] * 12
    nx_tomo.instrument.detector.data = numpy.empty(shape=(12, 10, 10))
    nx_tomo.sample.rotation_angle = numpy.linspace(0, 20, num=12)

    file_path = os.path.join(tmp_path, "nxtomo.nx")
    entry = "entry0000"
    nx_tomo.save(
        file_path=file_path,
        data_path=entry,
    )
    # delete some path that can be missing in some case
    with h5py.File(file_path, mode="a") as h5f:
        assert "entry0000" in h5f
        assert "entry0000/beam" not in h5f
        assert "entry0000/instrument/beam" not in h5f
        assert "entry0000/instrument/detector/distance" not in h5f
        assert "entry0000/instrument/detector/x_pixel_size" not in h5f
        assert "entry0000/instrument/detector/y_pixel_size" not in h5f
        assert "entry0000/instrument/detector/transformations" not in h5f

    scan = NXtomoScan(file_path, entry)

    # create the widget and do the edition
    widget = NXtomoEditor()

    widget.setScan(scan=scan)

    widget._distanceMetricEntry.setValue(0.05)
    widget._energyEntry.setValue(50)
    widget._xPixelSizeMetricEntry.setValue(0.02)
    widget._yPixelSizeMetricEntry.setValue(0.03)

    # overwrite the NXtomo
    task = NXtomoEditorTask(
        inputs={
            "data": scan,
            "configuration": widget.getConfigurationForTask(),
        }
    )
    task.run()

    # check save went well
    overwrite_nx_tomo = NXtomo().load(
        file_path=file_path,
        data_path=entry,
    )
    assert overwrite_nx_tomo.instrument.detector.x_pixel_size.value == 0.02
    assert overwrite_nx_tomo.instrument.detector.y_pixel_size.value == 0.03
    assert overwrite_nx_tomo.energy.value == 50
    assert overwrite_nx_tomo.instrument.detector.distance.value == 0.05
