import dataclasses

import typeguard

from exasol.analytics.schema.column_name import ColumnName
from exasol.analytics.schema.column_type import ColumnType
from exasol.analytics.utils.data_classes_runtime_type_check import check_dataclass_types


@dataclasses.dataclass(frozen=True, repr=True, eq=True)
class Column:
    name: ColumnName
    type: ColumnType

    def __post_init__(self):
        check_dataclass_types(self)
