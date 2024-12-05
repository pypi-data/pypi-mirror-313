import logging
import os

from orangewidget.settings import Setting

_logger = logging.getLogger(__name__)


class NXTomomillMixIn:
    """
    MixIn class for nxtomomill + ewoks
    """

    _scans = Setting(list())

    _ewoks_default_inputs = Setting(dict())

    CONFIG_CLS = None
    # logger to be used. Expected to be redefine by child class

    LOGGER = None
    # logger to be used. Expected to be redefine by child class

    def __init__(self, *args, **kwargs) -> None:
        self.__configuration_cache = None
        # cache updated for each folder in order to match `_execute_ewoks_task` design

    def add(self, *args, **kwargs):
        self.widget.add(*args, **kwargs)

    def _updateSettings(self):
        raise NotImplementedError("Base class")

    def _saveNXTomoCfgFile(self, cfg_file, keyword: str):
        """save the nxtomofile to the setttings"""
        assert (
            self.CONFIG_CLS is not None
        ), "inheriting classes are expected to redefine CONFIG_CLS"
        self._ewoks_default_inputs["nxtomomill_cfg_file"] = (
            cfg_file  # pylint: disable=E1137
        )

        if os.path.exists(cfg_file):
            try:
                configuration = self.CONFIG_CLS.from_cfg_file(
                    cfg_file
                )  # pylint: disable=E1102
            except Exception as e:
                self._logger.error(
                    f"Fail to use configuration file {cfg_file}. Error is {e}. No conversion will be done."
                )
            else:
                default_inputs = {
                    keyword: configuration.to_dict(),
                }
        else:
            default_inputs = {
                keyword: self.CONFIG_CLS().to_dict(),  # pylint: disable=E1102
            }

        # hack: try to upgrade x_pixel_keys and y_pixels keys to list.
        # otherwise has they have the same values and are tuples they have the same id and orange raises an
        # dump_literals raise a ValueError - check_relaxed - is a recursive structure
        try:
            default_inputs[keyword]["KEYS_SECTION"]["x_pixel_keys"] = list(
                default_inputs[keyword]["KEYS_SECTION"]["x_pixel_keys"]
            )
            default_inputs[keyword]["KEYS_SECTION"]["y_pixel_keys"] = list(
                default_inputs[keyword]["KEYS_SECTION"]["y_pixel_keys"]
            )
        except KeyError:
            pass

        self.update_default_inputs(
            **default_inputs,
        )

    def _get_task_arguments(self):
        adict = super()._get_task_arguments()
        # pop progress as does not fully exists on the orange-widget-base
        adict.pop("progress", None)
        return adict

    def __new__(cls, *args, **kwargs):
        # ensure backward compatibility with 'static_input'
        static_input = kwargs.get("stored_settings", {}).get("static_input", None)
        if static_input not in (None, {}):
            _logger.warning(
                "static_input has been deprecated. Will be replaced by _ewoks_default_inputs in the workflow file. Please save the workflow to apply modifications"
            )
            kwargs["stored_settings"]["_ewoks_default_inputs"] = static_input
        return super().__new__(cls, *args, **kwargs)
