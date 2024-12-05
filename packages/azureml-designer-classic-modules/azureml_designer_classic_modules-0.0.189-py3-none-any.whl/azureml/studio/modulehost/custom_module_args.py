import json
import urllib


class CustomModuleArguments:
    def __init__(self, input_paths, input_schema_paths, output_paths, output_schema_paths,
                 custom_script, parameters: dict = {}):
        self.input_paths = input_paths
        self.input_schema_paths = input_schema_paths
        self.output_paths = output_paths
        self.output_schema_paths = output_schema_paths
        self.custom_script = custom_script
        if parameters:
            self.parameters = parameters

    def encoded_in_json(self):
        json_format = json.dumps(self.__dict__)
        return urllib.parse.quote(json_format)
