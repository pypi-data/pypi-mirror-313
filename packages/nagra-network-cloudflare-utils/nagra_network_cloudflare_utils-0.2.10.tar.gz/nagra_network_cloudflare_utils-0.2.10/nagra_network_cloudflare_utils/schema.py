import logging
from typing import Literal, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    StrictBool,
    TypeAdapter,
    field_validator,
)

from .schema_utils import group, is_sorted

log = logging.getLogger("Validation")

PROXIED_VALUES = Literal["false", "true"]
TYPES_VALUES = Literal[
    "A",
    "AAAA",
    "CNAME",
    "MX",
    "TXT",
    "CAA",
    "SRV",
    "PTR",
    "SOA",
    "NS",
    "DS",
    "DNSKEY",
    "LOC",
    "NAPTR",
    "SSHFP",
    "SVCB",
    "TSLA",
    "URI",
    "SPF",
]


def check_duplicates(records):
    grouped = group(records, lambda r: r.name)
    grouped = {k: v for k, v in grouped.items() if len(v) > 1}
    if not grouped:
        return
    duplicates = []
    for name, records in grouped.items():
        # Some entries can be duplicated
        types = {r.type for r in records}
        types -= {"MX", "TXT"}  # They can be added along with any other
        # A and AAAA records are compatible
        if any(t in types for t in ("A", "AAAA")):
            types -= {"A", "AAAA"}
            if types:
                duplicates.append(name)
        # We can have multiple value for NS records
        if "NS" in types and len(types) > 1:
            duplicates.append(name)
    if not duplicates:
        log.warn(
            (
                "There are duplicate entries," "be sure that it is what you want:\n{}"
            ).format("\n".join(grouped.keys()))
        )
        return
    duplicates_str = "\n".join(duplicates)
    msg = f"""\
The following records have duplicates
Note that some records can be duplicated (e.g. A, AAAA, NS),
and some types are compatibles (e.g. A and AAAA):
{duplicates_str}
"""
    log.error(msg)
    raise Exception(msg)


# Same schema to validate tfplan.json, Cloudflare output and the csv file
class Record(BaseModel):
    # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = None
    name: str
    type: TYPES_VALUES
    value: str = Field(alias="content")
    ttl: PositiveInt
    proxied: Union[StrictBool, PROXIED_VALUES]

    @field_validator("name")
    def no_trailing_dot(cls, value):
        if value.strip().endswith("."):
            raise ValueError('dns entry are not allowed to end with a "."')
        return value

    def get_uuid(self):
        return (self.name, self.value)

    def __str__(self):
        return f"{self.name}, {self.type}, {self.value}"


RecordList = TypeAdapter(list[Record])


def check_records(records):
    records = RecordList.validate_python(records)  # model_validate
    check_duplicates(records)
    if not is_sorted(records, key=lambda x: x.name):
        # NOTE: This must not fail the pipeline. This is an additional warning
        # The error is located where the data are defined.
        log.warn("Records are not sorted, please sort them")
    return records


def sort_records(records):
    yield from sorted(records, key=lambda r: (r["name"], r["type"], r["content"]))
