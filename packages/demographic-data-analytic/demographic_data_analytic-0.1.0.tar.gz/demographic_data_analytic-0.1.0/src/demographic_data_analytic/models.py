import functools
import re
from collections import deque
from types import Callable
from types import MappingProxyType

import attrs
from attrs import define
from attrs import field
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql import types as T


PySparkTypes = MappingProxyType(
    {"Character": T.StringType(), "Numeric": T.DecimalType(38, 6), "Date": T.DateType()}
)


def normalize_column(column: str, strict: bool = False) -> str:
    RE_PUNCTUATION: str = r"[\s\.]+"
    pattern = re.compile(f"(^{RE_PUNCTUATION}|{RE_PUNCTUATION}$)")
    column = pattern.sub("", column.strip())
    if not strict:
        return column.replace(".", " ")
    return re.compile(RE_PUNCTUATION).sub("_", column.lower())


def parameter(parameter_type: type, parameter_mapping: str) -> attrs.Attribute:
    return field(
        metadata={"type": parameter_type, "alias": parameter_mapping.replace(".", " ")}
    )


def file_exists(directory: str, fs_func: Callable) -> Callable:
    def closure(instance, attribute, value) -> bool:
        files = fs_func(directory, recursive=False, only_files=True)
        if len(files) < 1:
            raise ValueError(f"Cannot find {value=} in {directory=}")
        return any(value in files for file in files)

    return closure


@define
class TidyDataModel:
    @classmethod
    def read(cls, *source: tuple[str], read_func: Callable) -> DataFrame:
        data = functools.reduce(DataFrame.unionByName, map(read_func, source))
        return data.withColumnsRenamed(
            {column: normalize_column(column) for column in data.columns}
        )

    @classmethod
    def transform(cls, data: DataFrame) -> DataFrame:
        queue = deque()
        for attr in attrs.fields(cls):
            column = F.col(field.metadata.get("alias")).alias(attr.name)
            column = column.cast(PySparkTypes.get(attr.metadata.get("type")))
            queue.append(column)
        return data.select(*queue)


@define
class MappingParameters:
    source: str = field(
        validator=[
            attrs.validators.instance_of(str),
            file_exists(
                directory="User Imported Data/EFT_UP/Sample Client/Input/Data Request Form"
            ),
        ]
    )

    def read(self, read_func: Callable) -> tuple:
        parameters = read_func(
            self.source, dataAddress="'Mapping_Parameters'!A1", header=True
        )
        return (
            self._initialize(parameters=parameters, period="prior"),
            self._initialize(parameters=parameters, period="current"),
        )

    def _parse(self, parameters: DataFrame, period: str) -> dict:
        def is_valid_mapping(record: dict, period: str) -> bool:
            INVALID_VALUES: tuple[str] = ("0.0", "#N/A", "")
            mapping = record.get(period, "0.0")
            return all(mapping != value for value in INVALID_VALUES)

        return [
            (
                normalize_column(record.get("Standard Header Name"), strict=True),
                record.get("Field Type"),
                record.get(period),
            )
            for record in parameters.pandas_api().to_dict(orient="records")
            if is_valid_mapping(record, period)
        ]

    def _initialize(self, parameters: list, period: str) -> attrs:
        match period:
            case "prior":
                period = "File Header Name_PY"
                class_name = "PriorPeriodCensus"
            case "current":
                period = "File Header Name_CY"
                class_name = "CurrentPeriodCensus"
            case _:
                raise ValueError("Must pass valid period: 'current' or 'prior'")
        parameters = self._parse(parameters, period)
        return attrs.make_class(
            class_name,
            {
                name: parameter(parameter_type=field_type, parameter_mapping=mapping)
                for (name, field_type, mapping) in parameters
            },
            bases=(TidyDataModel,),
        )
