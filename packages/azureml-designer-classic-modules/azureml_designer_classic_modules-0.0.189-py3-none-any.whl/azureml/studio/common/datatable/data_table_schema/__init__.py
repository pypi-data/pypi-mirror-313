from azureml.studio.core.data_frame_schema import DataFrameSchema as DataTableSchema
from azureml.studio.core.data_frame_schema import SchemaConstants, ColumnAttribute, FeatureChannel
from azureml.studio.core.utils.labeled_list import LabeledList

# NOTICE! PLEASE DO NOT USE THIS PACKAGE!
# This package is added for back-compatibility of legacy module:
#   azureml.studio.common.datatable.data_table_schema,
# which should be only used in legacy pickled object deserialization.
#
# Please DON'T add any new scripts to this package.
# Please DON'T modify this __init__.py unless necessary.
# Please DON'T use/import the classes that declared in this module.

# This _dummy_import_list is only for make explicit references from the declared classes
# that renamed from azureml.studio.core classes.
# It shouldn't be used in anywhere for any purposes.
_dummy_import_list = [
    DataTableSchema,
    SchemaConstants,
    ColumnAttribute,
    FeatureChannel,
    LabeledList,
]
