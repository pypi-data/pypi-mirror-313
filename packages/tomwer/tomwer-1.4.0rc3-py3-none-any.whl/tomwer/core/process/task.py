"""
Define the tomwer Task class.
Insure connection with ewoks.
All instances of tomwer Tasks should avoid gui import (as qt).
"""

from __future__ import annotations

import logging
from collections import namedtuple
from datetime import datetime

import h5py
import numpy
from ewokscore.task import Task as _EwoksTask
from ewokscore.taskwithprogress import TaskWithProgress as _EwoksTaskWithProgress
from silx.io.dictdump import dicttoh5, h5todict
from silx.io.utils import h5py_read_dataset
from silx.io.utils import open as open_hdf5
from tomoscan.io import HDF5File
from tomwer.core.utils.locker import FileLockerManager


_logger = logging.getLogger(__name__)

_process_desc = namedtuple(
    "_process_desc", ["process_order", "configuration", "results"]
)


class BaseProcessInfo:
    """Tomwer base process class"""

    _output_values = {}
    # TODO: look at this: not sure this is needed anymore

    def __init__(self, inputs=None):
        """
        :param return_dict: if True serialize (to_dict / from_dict functions) between each task
        """
        if inputs is None:
            inputs = {}

        self._scheme_title = (
            "scheme_title"  # TODO: have a look, this must be get somewhere and reused ?
        )

        """should the return type of the handler should be TomoBase instance
        objects or dict"""
        self._settings = {}
        self._cancelled = False
        # a useful variable that can be set to True if the task has been cancelled

    @staticmethod
    def properties_help():
        """

        :return: display the list of all managed keys and possible values
        """
        # TODO: use argsparse instead of this dict ?
        raise NotImplementedError("BaseProcess is an abstract class")

    def get_output_value(self, key):
        """

        :param key:
        :return:
        """
        assert type(key) is str
        if key in self._output_values:
            return self._output_values[key]
        else:
            return None

    def clear_output_values(self):
        self._output_values.clear()

    def register_output(self, key, value):
        """

        :param key: name of the output
        :param value: value of the output
        """
        self._output_values[key] = value

    @staticmethod
    def program_name():
        """Name of the program used for this processing"""
        raise NotImplementedError("Base class")

    @staticmethod
    def program_version():
        """version of the program used for this processing"""
        raise NotImplementedError("Base class")

    @staticmethod
    def definition():
        """definition of the process"""
        raise NotImplementedError("Base class")

    def get_configuration(self) -> dict | None:
        """

        :return: configuration of the process
        """
        if self._settings is None:
            return None
        if len(self._settings) > 0:
            return self._settings
        else:
            return None

    def set_configuration(self, configuration: dict) -> None:
        self._settings = configuration

    def register_process(
        self,
        process_file: str,
        entry: str,
        configuration: dict | None,
        results: dict | None,
        process_index: int,
        interpretations: dict | None = None,
        overwrite: bool = True,
    ) -> None:
        """
        Store the current process in the linked h5 file if any,
        output data stored will be the one defined by the data_keys

        :param process_file: where to store the processing information
        :param entry: entry process
        :param configuration: configuration of the process
        :param results: result of the processing
        :param process_index: index of the process
        :param overwrite: if True then overwrite the process if already
                               exists
        :paramerpretations: for each result we can add a flag
                                'interpretation'
        """
        assert process_file is not None
        with FileLockerManager().get_lock(file_name=process_file):
            try:
                self._register_process(
                    process_file=process_file,
                    entry=entry,
                    process=self,
                    configuration=configuration,
                    results=results,
                    process_index=process_index,
                    interpretations=interpretations,
                    overwrite=overwrite,
                )
            except IOError as e:
                _logger.error(e)

    @staticmethod
    def _register_process(
        process_file: str,
        process,
        entry: str | None,
        configuration: dict | None,
        results: dict | None,
        process_index: int,
        interpretations: dict | None = None,
        overwrite: bool = True,
    ) -> None:
        """
        Store the current process in the linked h5 file if any,
        output data stored will be the one defined by the data_keys

        :param process: process to record
        :param process_file: where to store the processing information
        :param entry: entry process
        :param configuration: configuration of the process
        :param results: result of the processing
        :param process_index: index of the process
        :param overwrite: if True then overwrite the process if already
                               exists
        :paramerpretations: for each result we can add a flag
                                'interpretation'
        """
        assert process_file is not None, "The process file should be defined"
        if interpretations is None:
            interpretations = {}
        process_name = "tomwer_process_" + str(process_index)

        def get_process_path():
            return "/".join((entry or "entry", process_name))

        # save it to the file (lock should be handled upper)
        with HDF5File(process_file, mode="a") as h5f:
            nx_process = h5f.require_group(get_process_path())
            if "NX_class" not in nx_process.attrs:
                nx_process.attrs["NX_class"] = "NXprocess"
            if overwrite:
                for key in (
                    "program",
                    "results",
                    "version",
                    "date",
                    "sequence_index",
                    "class_instance",
                    "configuration",
                ):
                    if key in nx_process:
                        del nx_process[key]

            # write process information
            nx_process["program"] = process.program_name()
            nx_process["version"] = process.program_version()
            nx_process["date"] = datetime.now().replace(microsecond=0).isoformat()
            nx_process["sequence_index"] = numpy.int32(process_index)
            _class = process.__class__
            nx_process["class_instance"] = ".".join(
                (_class.__module__, _class.__name__)
            )

        # dump result
        if results is not None:
            h5path = "/".join((get_process_path(), "results"))
            dicttoh5(
                results,
                h5file=process_file,
                h5path=h5path,
                update_mode="modify",
                mode="a",
            )
            for interpretation_key, interpretation in interpretations.items():
                try:
                    with HDF5File(process_file, mode="a") as h5f:
                        node = h5f["/".join((get_process_path(), "results"))]
                        node[interpretation_key].attrs[
                            "interpretation"
                        ] = interpretation
                except KeyError:
                    _logger.warning(
                        "Invalid interpretation - no result store"
                        " for %s" % interpretation_key
                    )

        # dump configuration
        if configuration is not None:
            h5path = "/".join((get_process_path(), "configuration"))
            dicttoh5(
                configuration,
                h5file=process_file,
                h5path=h5path,
                update_mode="modify",
                mode="a",
            )

            with HDF5File(process_file, mode="a") as h5f:
                nx_process = h5f.require_group(get_process_path())
                nx_process["configuration"].attrs["NX_class"] = "NXcollection"

    @staticmethod
    def _get_process_nodes(
        root_node: h5py.Group, process, version: str = None, depth: int = 2
    ) -> dict:
        """

        :param root_node:
        :param version: version to look for (ignored for now)
        :return: list of process nodes [as h5py.Group]. Key is node name,
                 value is the process index
        """

        def is_process_node(node):
            if node is None:
                return False
            return (
                node.name.split("/")[-1].startswith("tomwer_process_")
                and "NX_class" in node.attrs
                and node.attrs["NX_class"] == "NXprocess"
                and "program" in node
                and (
                    process is None
                    or h5py_read_dataset(node["program"]) == process.program_name()
                )
                and "version" in node
                and "sequence_index" in node
            )

        if isinstance(root_node, h5py.Dataset):
            return {}
        res = {}
        if is_process_node(root_node):
            res[root_node.name] = int(h5py_read_dataset(root_node["sequence_index"]))

        if root_node is not None:
            for _, node in root_node.items():
                if depth >= 1:
                    res.update(
                        Task._get_process_nodes(
                            process=process,
                            root_node=node,
                            depth=depth,
                            version=version,
                        )
                    )
        return res

    @staticmethod
    def get_most_recent_process(
        root_node: h5py.Group, process, version: str = None
    ) -> h5py.Group | None:
        nodes = Task._get_process_nodes(
            root_node=root_node, process=process, version=version, depth=1
        )
        nodes_with_time = []
        nodes_time = []
        import datetime

        for node_name in nodes:
            node = root_node[node_name]
            assert isinstance(node, h5py.Group), "node should be a h5py.Group"
            if "date" in node:
                nodes_with_time.append(node)
                nodes_time.append(
                    datetime.datetime.fromisoformat(h5py_read_dataset(node["date"]))
                )
        if len(nodes_with_time) == 0:
            return None
        else:
            st = numpy.argmax(nodes_time)
            return nodes_with_time[st]

    @staticmethod
    def get_processes_frm_type(process_file: str, process_type, entry=None) -> list:
        """

        :param process_file: file to read
        :param process_type: process type we are looking for
        :return: list of _process_desc(sequence_index, configuration, results)
        """
        # retrieve process to load
        with open_hdf5(process_file) as h5f:
            if entry is None:
                if len(h5f.keys()) > 0:
                    root = h5f[list(h5f.keys())[0]]
                else:
                    _logger.warning("no process find")
                    return []
            else:
                root = h5f[entry]

            processes_to_load = {}
            for process in root.keys():
                nx_process = root[process]
                if (
                    h5py_read_dataset(nx_process["program"])
                    == process_type.program_name()
                ):
                    processes_to_load[nx_process.name] = h5py_read_dataset(
                        nx_process["sequence_index"]
                    )

        # load process
        processes = []
        for process_name, p_order in processes_to_load.items():
            config = h5todict(process_file, "/".join((process_name, "configuration")))
            results = h5todict(process_file, "/".join((process_name, "results")))
            processes.append(
                _process_desc(
                    process_order=p_order, configuration=config, results=results
                )
            )
        return processes


class TaskWithProgress(_EwoksTaskWithProgress, BaseProcessInfo):
    """Class from which all tomwer process should inherit

    :param logger: the logger used by the class
    """

    def __init__(
        self,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
        progress=None,
    ):
        BaseProcessInfo.__init__(self, inputs=inputs)
        _EwoksTaskWithProgress.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
            progress=progress,
        )


class Task(_EwoksTask, BaseProcessInfo):
    """Class from which all tomwer process should inherit

    :param logger: the logger used by the class
    """

    def __init__(
        self,
        varinfo=None,
        inputs=None,
        node_id=None,
        node_attrs=None,
        execinfo=None,
    ):
        BaseProcessInfo.__init__(self, inputs=inputs)
        _EwoksTask.__init__(
            self,
            varinfo=varinfo,
            inputs=inputs,
            node_id=node_id,
            node_attrs=node_attrs,
            execinfo=execinfo,
        )
