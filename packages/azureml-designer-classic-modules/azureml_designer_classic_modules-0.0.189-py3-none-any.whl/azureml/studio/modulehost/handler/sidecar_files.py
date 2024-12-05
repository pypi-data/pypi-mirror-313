import json
from enum import Enum
from typing import TextIO

from azureml.studio.core.io.data_frame_visualizer import DataFrameVisualizer
from azureml.studio.common.datatable.data_table import DataTable
from azureml.studio.internal.io.rwbuffer_manager import AzureMLOutput
from azureml.studio.common.json_encoder import EnhancedJsonEncoder
from azureml.studio.modules.ml.common.report_data_json_converter import ReportDataJsonConverter
from azureml.studio.core.logger import common_logger, TimeProfile
from azureml.studio.core.utils.fileutils import make_file_name, make_full_path
from azureml.studio.modules.datatransform.common.base_transform import BaseTransform
from azureml.studio.modules.ml.common.base_clustser import BaseCluster
from azureml.studio.modules.ml.common.base_learner import BaseLearner


class SideCarFileType(Enum):
    METADATA = 'metadata'
    VISUALIZATION = 'visualization'
    SCHEMA = 'schema'
    RUNTIME_INFO = 'runtimeinfo'


class VisualizationType(Enum):
    DEFAULT = 'default'
    BINARY_CLASSIFIER_EVALUATION_COMPARISION = 'binaryClassifierEvaluationComparison'
    # TODO: add more types


class SideCarFile:
    def __init__(self, file_type: SideCarFileType):
        self._file_type = file_type

    @property
    def file_type(self):
        return self._file_type

    @property
    def file_type_name(self):
        return self.file_type.value

    @property
    def file_extension(self):
        return self.file_type.value

    def dump_to_dict(self):
        # Supposed to be implemented in subclasses
        return {}

    def dump(self, file: TextIO):
        data = self.dump_to_dict()
        json.dump(data, file, indent=2, cls=EnhancedJsonEncoder)


class SchemaDumper(SideCarFile):
    def __init__(self):
        super().__init__(file_type=SideCarFileType.SCHEMA)


class DataFrameSchemaDumper(SchemaDumper):
    def __init__(self, data_table: DataTable):
        super().__init__()
        self._data_table = data_table

    def dump_to_dict(self):
        return self._data_table.meta_data.to_dict()


class Visualizer(SideCarFile):
    def __init__(self, visualization_type=VisualizationType.DEFAULT):
        super().__init__(file_type=SideCarFileType.VISUALIZATION)
        self._visualization_type = visualization_type


class DataTableVisualizer(Visualizer):
    def __init__(self, data_table: DataTable):
        super().__init__()
        self._data_table = data_table

    def dump_to_dict(self):
        return DataFrameVisualizer(
            self._data_table.data_frame,
            schema=self._data_table.meta_data.to_dict(),
            compute_stats=True,
        ).json_data


class LearnerVisualizer(Visualizer):
    def __init__(self, learner: BaseLearner):
        super().__init__()
        self._learner = learner

    def dump_to_dict(self):
        raise NotImplementedError("Visualization not supported for BaseLearner currently")


class ClusterVisualizer(Visualizer):
    def __init__(self, cluster: BaseCluster):
        super().__init__()
        self._cluster = cluster

    def dump_to_dict(self):
        raise NotImplementedError("Visualization not supported for BaseCluster currently")


class BinaryClassifierEvaluationComparisionVisualizer(Visualizer):
    _CONVERTER = ReportDataJsonConverter()

    def __init__(self, *reports):
        super().__init__(VisualizationType.BINARY_CLASSIFIER_EVALUATION_COMPARISION)
        self._reports = reports

    def dump_to_dict(self):
        return {
            'visualizationType': self._visualization_type.value,
            'reports': self._report_list_to_dict(*self._reports),
        }

    def _report_list_to_dict(self, *reports):
        return [self._report_to_dict(r) for r in reports if r is not None]

    def _report_to_dict(self, report):
        return self._CONVERTER.report_to_dict(report)


class RuntimeInfo(SideCarFile):
    def __init__(self):
        super().__init__(file_type=SideCarFileType.RUNTIME_INFO)


class SideCarFileBundle:
    def __init__(self, data, *, schema_dumper=None, visualizer=None, runtime_info=None):
        self._data = data
        self._schema_dumper = schema_dumper
        self._visualizer = visualizer
        self._runtime_info = runtime_info

    @classmethod
    def create(cls, obj, *, schema_dumper=None, visualizer=None, runtime_info=None):
        if isinstance(obj, DataTable):
            return SideCarFileBundle(
                obj,
                schema_dumper=schema_dumper,
                visualizer=visualizer or DataTableVisualizer(data_table=obj),
            )
        elif isinstance(obj, BaseLearner):
            return SideCarFileBundle(
                obj,
                # TODO: to be implemented
                # LearnerVisualizer(learner=obj),
            )
        elif isinstance(obj, BaseCluster):
            return SideCarFileBundle(
                obj,
                # TODO: to be implemented
                # ClusterVisualizer(cluster=obj),
            )
        elif isinstance(obj, BaseTransform):
            return SideCarFileBundle(
                obj,
                # TODO: to be implemented
                # LearnerVisualizer(learner=obj),
            )
        else:
            # Create empty SideCarFileBundle for unrecognized data types.
            # Do not raise error here. Be gentle, be graceful.
            common_logger.warning(f"Created empty SideCarBundle for unrecognized data type {type(obj)}.")
            return SideCarFileBundle(obj)

    @property
    def data(self):
        return self._data

    @property
    def sidecar_files(self):
        return (f for f in (self._schema_dumper, self._visualizer, self._runtime_info) if f is not None)

    @property
    def visualizer(self):
        return self._visualizer

    def dump_sidecar_files(self, dumpers: list, file_name):
        for dumper in dumpers:
            for sf in self.sidecar_files:
                dumper.dump(sf)


class FileDumper:
    def __init__(self, file_path, file_name):
        self.path = file_path
        self.name = file_name

    def dump(self, sf):
        sf_full_path = make_full_path(self.path, self.name, sf.file_extension)
        full_file_name = make_file_name(self.name, sf.file_extension)
        with TimeProfile(f"Create sidecar file '{full_file_name}'"):
            with open(sf_full_path, 'w') as f:
                sf.dump(f)


class AzureMLOutputDumper:
    def __init__(self, folder, file_name, run=None):
        self.run = run
        self.folder = folder
        self.name = file_name

    def dump(self, sf):
        sf_path = make_full_path(self.folder, self.name, sf.file_extension)
        with TimeProfile(f"Upload sidecar file '{sf_path}'"):
            with AzureMLOutput.open(sf_path, 'w', self.run) as fout:
                sf.dump(fout)
