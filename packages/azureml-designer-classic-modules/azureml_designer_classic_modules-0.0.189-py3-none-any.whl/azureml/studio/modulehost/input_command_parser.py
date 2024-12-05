from uuid import UUID

from azureml.studio.common.datatypes import DataTypes
from azureml.studio.core.utils.dictutils import get_value_by_key_path
from azureml.studio.core.utils.strutils import generate_cls_str, join_stripped
from azureml.studio.modulehost.module_reflector import ModuleEntry


class InputPortValue:
    """
    To store the input port info, such as name, folder and extra folder for the sidecar files
    """
    def __init__(self, input_port_dict: dict):
        self._dct = input_port_dict

        extra_output = None
        if 'ExtraOutputInfo' in input_port_dict:
            if isinstance(input_port_dict['ExtraOutputInfo'], dict) and 'Folder' in input_port_dict['ExtraOutputInfo']:
                extra_output = input_port_dict['ExtraOutputInfo']['Folder']

        self.name = input_port_dict.get('Name')
        self.folder = input_port_dict.get('Folder')
        self.extra_folder = extra_output

        self.data_source_id = input_port_dict.get('DataSourceId')
        self.model_id = input_port_dict.get('TrainedModelId')
        self.transform_id = input_port_dict.get('TransformModuleId')

    @property
    def file_name(self):
        return get_value_by_key_path(self._dct, 'InputFileInfo/Name')

    @property
    def data_type(self):
        data_type_name = get_value_by_key_path(self._dct, 'InputFileInfo/DataTypeId')
        if not data_type_name:
            return None
        return DataTypes.from_name(data_type_name)

    @property
    def blob_info(self):
        return self._dct.get('ExternalInputFileInfo')

    @property
    def blob_container_name(self):
        return self.blob_info.get('ContainerName') if self.blob_info else None

    @property
    def blob_path(self):
        return self.blob_info.get('FilePath') if self.blob_info else None

    @property
    def datastore_name(self):
        return self.blob_info.get('DataStoreName') if self.blob_info else None

    @property
    def is_global_datastore(self):
        return self.datastore_name == 'smtprodeastus1globaluploadedresources'

    def __str__(self):
        folder = self.folder
        extra_folder = f"(extra_folder={self.extra_folder})" if self.extra_folder else None
        return generate_cls_str(self, folder, extra_folder, with_obj_id=False)


class InputCommandParser:
    """
    Extract information from JES execution command file
    (passed to module host from the --command-file argument)
    for ModuleHost usage.
    """

    def __init__(self, input_dict):
        """
        :param command: Input dict when invoked from JES for execution, something like the following:
        ```
        {
            "Id": "e5aa3e71-1f92-4ea2-a1c4-6a1572bc3422-376",
            "ModuleId": "506153734175476c4f62416c57734963.401b4f92e7244d5abe81d5b0ff9bdb33.v1-default-1751",
            "ModuleEntry": {
                "ModuleName": "azureml.studio.modules.ml.score.score_generic_module.score_generic_module",
                "ClassName": "ScoreModelModule",
                "MethodName": "run"
            },
            "ModuleParameters": [
                {
                    "Name": "Append score columns to output",
                    "Value": "True",
                    "ValueType": "Literal",
                    "LinkedGlobalParameter": null
                },
                {
                    "Name": "Please Specify Data Source",
                    "Value": "Microsoft Azure BLOB Storage",
                    "ValueType": "Literal",
                    "LinkedGlobalParameter": null
                },
                {
                    "Name": "URL",
                    "Value": "http://www.microsoft.com",
                    "ValueType": "Literal",
                    "LinkedGlobalParameter": null
                },
                {
                    "Name": "Data Format",
                    "Value": "CSV",
                    "ValueType": "Literal",
                    "LinkedGlobalParameter": null
                },
                {
                    "Name": "CSV or TSV has Header Row",
                    "Value": "False",
                    "ValueType": "Literal",
                    "LinkedGlobalParameter": null
                },
            ],
            "InputPortsInternal": [
                {
                    "Name": "Trained model",
                    "Folder": "4cfda5ac-c51b-4782-a79d-562cb07a6792",
                    "InputFileInfo": {
                        "DataTypeId": "GenericCSVNoHeader",
                        "Name": "data.csv"
                    }
                },
                {
                    "Name": "Dataset",
                    "Folder": "2a8320c6-7ee4-4bfe-991b-ad82c62faaa0",
                    "InputFileInfo": {
                        "DataTypeId": "GenericCSVNoHeader",
                        "Name": "data.csv"
                    }
                }
            ],
            "OutputPortsInternal": [
                {
                    "Name": "Scored dataset",
                    "Folder": "ee4fd6cf-31fc-4720-9711-9ded6eb5976d"
                }
            ],
            "ModuleStatisticsFolder": "9425a71e-4c53-11e9-8646-d663bd873d93",
            "UsePreviousResults": false,
            "IsPartOfPartialRun": null,
            "Comment": "",
            "CommentCollapsed": true
        }
        ```

        """
        self._dct = input_dict
        self._module_info = input_dict['ModuleEntry']
        self._module_id = input_dict['ModuleId']
        self._params = input_dict['ModuleParameters'] or {}
        self._input_ports = input_dict['InputPortsInternal'] or {}
        self._output_ports = input_dict['OutputPortsInternal'] or {}
        self._module_statistics_folder = input_dict.get('ModuleStatisticsFolder', None)

    def to_name_value_dict(self):
        """
        Generate the parameter ("Name": "Value") dict from the self._params, self._input_ports list.
        For the input example, this method will generate the dict like the following:

        ```
        {
            "Dataset0": "input0.dataset",
            "Dataset1": "input1.dataset",
        }
        ```

        :return: The generated dict.
        """
        pass

    @property
    def node_id(self):
        """
        Return the following value from dict.
        ```
        "Id": "e5aa3e71-1f92-4ea2-a1c4-6a1572bc3422-376",
        ```
        """
        return self._dct.get('Id')

    @property
    def node_short_id(self):
        """
        Extract last part from node_id.

        Example:
            For Id: "e5aa3e71-1f92-4ea2-a1c4-6a1572bc3422-376", return "376"

        :return:
        """
        try:
            return self.node_id.split('-')[-1]
        except BaseException:
            return ''

    @property
    def module_entry(self):
        """
        :return: A ModuleEntry instance.
        """
        return ModuleEntry.from_dict(self._module_info)

    @property
    def module_family_id(self):
        """
        Get module family id from ModuleId field.

        Format:
            WorkSpaceId.FamilyId.Version-Culture-Batch
        Sample:
            506153734175476c4f62416c57734963.4e1b0fe6aded4b3fa36f39b8862b9004.v1-default-153
        :return: Extract FamilyId part from ModuleId string, parsed into an UUID object.
        """
        return UUID(self._module_id.split('.')[1])

    @property
    def param_dict(self):
        """
        Returns a 'Name':'Value' dict of parameters, where value is in string format.

        Example:
        ```
        {
            "Append score columns to output": "True",
            "Please Specify Data Source": "Microsoft Azure BLOB Storage",
            "URL": "http://www.microsoft.com",
            "Data Format": "CSV",
            "CSV or TSV has Header Row": "False",
        }
        ```

        :return: the dict contains parameter's key and values.

        """
        return {p['Name']: p['Value'] for p in self._params if not p.get('IsSensitiveField', False)}

    @property
    def input_port_dict(self):
        """
        Returns a 'Name': InputPortValue instance dict of input ports.

        Example:
        ```
        {
            "Trained model": "4cfda5ac-c51b-4782-a79d-562cb07a6792",
            "Dataset": "2a8320c6-7ee4-4bfe-991b-ad82c62faaa0",
            "ExtraOutputInfo": {
                "Folder": "ecfbbb81fa574528b1939a2e384bf554-1"
            }
        }
        ```
        :return: the dict contains input port's key,and InputPortValue instance.
        """

        return {x['Name']: InputPortValue(x) for x in self._input_ports}

    @property
    def output_port_dict(self):
        """
        Returns a 'Name':'Folder' dict of output ports.

        Example:
        ```
        {
            "Scored dataset": "ee4fd6cf-31fc-4720-9711-9ded6eb5976d",
        }
        ```
        :return: the dict contains output port's key and folder.
        """
        return {p['Name']: p['Folder'] for p in self._output_ports}

    @property
    def module_statistics_folder(self):
        return self._module_statistics_folder

    @property
    def short_description(self):
        short_class_name = self.module_entry.class_name[:-len('Module')]
        return join_stripped(short_class_name, self.node_short_id, sep='-')

    def __str__(self):
        return generate_cls_str(self, self.short_description, with_obj_id=False)
