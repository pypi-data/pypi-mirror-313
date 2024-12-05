import json
import os
from enum import Enum

from azureml.studio.common.mixins import MetaExtractMixin


class DataType(MetaExtractMixin):
    __slots__ = ('_id', '_name', '_short_name', '_ws20_name', '_description', '_is_directory', '_owner',
                 '_file_extension', '_content_type', '_allow_upload', '_allow_promotion', '_allow_model_promotion',
                 '_auxiliary_file_extension', '_auxiliary_content_type')

    def __init__(self, data_type_name, name, short_name=None, ws20_name=None, description=None, is_directory=False,
                 owner="Microsoft Corporation", file_extension="", content_type="",
                 allow_upload=True, allow_promotion=True, allow_model_promotion=False,
                 auxiliary_file_extension=None, auxiliary_content_type=None):
        self._id = data_type_name
        self._name = name
        self._short_name = short_name if short_name else data_type_name
        self._ws20_name = ws20_name
        self._description = description
        self._is_directory = is_directory
        self._owner = owner
        self._file_extension = file_extension
        self._content_type = content_type
        self._allow_upload = allow_upload
        self._allow_promotion = allow_promotion
        self._allow_model_promotion = allow_model_promotion
        self._auxiliary_file_extension = auxiliary_file_extension
        self._auxiliary_content_type = auxiliary_content_type

    @property
    def name(self):
        return self._id

    @property
    def short_name(self):
        return self._short_name

    @property
    def ws20_name(self):
        """The name used in Workspace 2.0"""
        return self._ws20_name if self._ws20_name else self.short_name

    @property
    def file_extension(self):
        return self._file_extension


class DataTypes(Enum):
    GENERIC_CSV = DataType(
        data_type_name="GenericCSV",
        name="Generic CSV File with a header",
        ws20_name="CsvFile",
        description="Comma-separated text file with a header",
        file_extension="csv",
        content_type="text/csv",
    )

    GENERIC_CSV_NO_HEADER = DataType(
        data_type_name="GenericCSVNoHeader",
        name="Generic CSV File With no header",
        ws20_name="CsvFile",
        description="Comma-separated text file with no header",
        file_extension="nh.csv",
        content_type="text/csv",
    )

    GENERIC_CSV_DIRECTORY = DataType(
        data_type_name="GenericCSVDirectory",
        name="Generic CSV Directory",
        ws20_name="AnyDirectory",
        description="Directory containing comma-separated text files with no header",
        is_directory=True,
        allow_upload=False,
    )

    GENERIC_TSV = DataType(
        data_type_name="GenericTSV",
        name="Generic TSV File with a header",
        ws20_name="CsvFile",
        description="Tab-separated text file with a header",
        file_extension="tsv",
        content_type="text/plain",
    )

    GENERIC_TSV_NO_HEADER = DataType(
        data_type_name="GenericTSVNoHeader",
        name="Generic TSV File With no header",
        ws20_name="CsvFile",
        description="Tab-separated text file with no header",
        file_extension="nh.tsv",
        content_type="text/plain",
    )

    GENERIC_TSV_DIRECTORY = DataType(
        data_type_name="GenericTSVDirectory",
        name="Generic TSV Directory",
        ws20_name="AnyDirectory",
        description="Directory containing tab-separated text files with no header",
        is_directory=True,
        allow_upload=False,
    )

    PLAIN_TEXT = DataType(
        data_type_name="PlainText",
        name="Plain Text",
        ws20_name="AnyFile",
        description="Plain text file",
        file_extension="txt",
        content_type="text/plain",
        allow_upload=False,
    )

    GENERIC_BINARY = DataType(
        data_type_name="GenericBinary",
        name="Generic Binary",
        ws20_name="AnyFile",
        description="A binary file",
        file_extension="bin",
        allow_upload=False,
    )

    GENERIC_HTML = DataType(
        data_type_name="GenericHtml",
        name="Generic HTML file",
        ws20_name="AnyFile",
        description="An HTML file",
        file_extension="htm",
        content_type="application/octet-stream",
        allow_upload=False,  # For security reasons we want to view the downloadable binary file instead of html.
    )

    # Will not be used in python version, but let's just leave it here.
    GENERIC_DOT_NET = DataType(
        data_type_name="GenericDotNet",
        name="Generic .NET file",
        description="A .NET serialized object",
        file_extension="net",
        content_type="application/octet-stream",
        allow_upload=False,
    )

    # Will not be used in python version, but let's just leave it here.
    DATATABLE_DOT_NET = DataType(
        data_type_name="DataTableDotNet",
        name="DataTable .NET file",
        description="A .NET serialized DataTable",
        file_extension="datatable",
        content_type="application/octet-stream",
        allow_upload=False,
    )

    DATASET = DataType(
        data_type_name="Dataset",
        name="Dataset .NET file",  # TODO: copied from v1. naming miss?
        ws20_name="DataFrameDirectory",
        description="A serialized DataTable supporting partial reads and writes",
        file_extension="dataset.parquet",
        content_type="application/octet-stream",
        allow_upload=False,
    )

    LEARNER = DataType(
        data_type_name="ILearnerDotNet",
        name="ILearner .NET file",
        short_name="Model",
        ws20_name="ModelDirectory",
        description="A .NET serialized ILearner",
        file_extension="ilearner",
        content_type="application/octet-stream",
        allow_upload=False,
        allow_promotion=False,
        allow_model_promotion=True,
    )

    FILTER = DataType(
        data_type_name="IFilterDotNet",
        name="IFilter .NET file",
        short_name="Filter",
        ws20_name="ModelDirectory",
        description="A .NET serialized IFilter",
        file_extension="ifilter",
        content_type="application/octet-stream",
        allow_upload=False,
        allow_promotion=False,
    )

    CLUSTER = DataType(
        data_type_name="IClusterDotNet",
        name="ICluster .NET file",
        short_name="Cluster",
        ws20_name="ModelDirectory",
        description="A .NET serialized ICluster",
        file_extension="icluster",
        content_type="application/octet-stream",
        allow_upload=False,
        allow_promotion=False,
        allow_model_promotion=True,
    )

    RECOMMENDER = DataType(
        data_type_name="IRecommenderDotNet",
        name="IRecommender .NET file",
        short_name="Recommender",
        ws20_name="ModelDirectory",
        description="A .NET serialized IRecommender",
        file_extension="irecommender",
        content_type="application/octet-stream",
        allow_upload=False,
        allow_promotion=False,
        allow_model_promotion=True,
    )

    TRANSFORM = DataType(
        data_type_name="ITransformDotNet",
        name="ITransform .NET file",
        short_name="Transform",
        ws20_name="TransformationDirectory",
        description="A .NET serialized ITransform",
        file_extension="itransform",
        content_type="application/octet-stream",
        allow_upload=False,
        allow_promotion=False,
        allow_model_promotion=True,
    )

    SVM_LIGHT = DataType(
        data_type_name="SvmLight",
        name="SvmLight File",
        description="A SvmLight file",
        file_extension="svmlight",
        content_type="text/plain",
        allow_upload=False,
    )

    ARFF = DataType(
        data_type_name="ARFF",
        name="Attribute Relation File Format",
        description="Attribute relation file format",
        file_extension="arff",
        content_type="text/plain",
        allow_upload=False,
    )

    EXCEL_WORKBOOK = DataType(
        data_type_name="ExcelWorkbook",
        name="Excel Workbook",
        description="Excel workbook",
        file_extension="xlsx",
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        allow_upload=False,
    )

    ZIP = DataType(
        data_type_name="Zip",
        name="Zip File",
        ws20_name="ZipFile",
        description="A zip file",
        file_extension="zip",
        content_type="application/zip",
    )

    R_OBJECT = DataType(
        data_type_name="RData",
        name="R Object or Workspace",
        description="A serialized R object",
        file_extension="RData",  # TODO: copied from v1. should be lower case?
        content_type="application/vnd.ms-rdata",
        allow_upload=False,
    )

    HIVE_TABLE = DataType(
        data_type_name="HiveTable",
        name="Hive Table",
        description="Hive Table on HDInsight",
        allow_upload=False,
        allow_promotion=False,
    )

    GENERIC_FOLDER = DataType(
        data_type_name="GenericFolder",
        name="Generic Folder",
        ws20_name="AnyDirectory",
        description="A generic folder contains any type of files",
        file_extension="folder",
        allow_upload=False,
        allow_promotion=True,
    )

    ANY = DataType(
        data_type_name="Any",
        name="Any Data",
        ws20_name="AnyDirectory",
        description="Data of any type",
        content_type="application/octet-stream",
        allow_upload=False,
    )

    @staticmethod
    def from_name(name):
        """Given a name of DataType, find a corresponding item in DataTypes enum.

        :param name: The name of DataType.
        :return: The corresponding item in DataTypes enum.
        """
        for e in DataTypes:
            if e.value.name == name:
                return e
        else:
            raise ValueError(f"Failed to load instance of DataTypes from dict")

    @staticmethod
    def from_extension(extension):
        """Given a extension string, find a corresponding item in DataTypes enum.

        :param extension: extension of file, with or without the leading dot.
        :return: The corresponding item in DataTypes enum.
        """
        extension = extension.strip('.')
        if not extension:
            raise ValueError(f"Unable to detect DataType: No file extension.")

        for e in DataTypes:
            if e.value.file_extension == extension:
                return e
        else:
            raise ValueError(f"Unable to detect DataType: Unrecognized file extension '.{extension}'.")

    @staticmethod
    def from_file_name(file_name):
        """Given a file name, detect DataType using file extension.

        :param file_name: file name, with or without full path
        :return: The corresponding item in DataTypes enum.
        """
        base_name = os.path.basename(file_name)

        stem_file_name, file_extension = os.path.splitext(base_name)
        _, secondary_extension = os.path.splitext(stem_file_name)

        # clear unrecognized secondary extensions
        if file_extension in ('.csv', '.tsv'):
            if secondary_extension != '.nh':
                secondary_extension = None

        elif file_extension == '.parquet':
            if secondary_extension != '.dataset':
                secondary_extension = None
        else:
            secondary_extension = None

        # append as file extension if secondary extension is not None
        if secondary_extension:
            file_extension = secondary_extension + file_extension

        return DataTypes.from_extension(file_extension)

    @staticmethod
    def from_json_file(file):
        with open(file) as f:
            d = json.load(f)
            return DataTypes.from_name(d.get('Id'))
