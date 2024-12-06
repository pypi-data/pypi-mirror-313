import logging
from typing import Iterable, Literal, Optional, Union

from nagra_network_misc_utils.gitlab import add_mr_comment
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


def check_ns_records(records: Iterable[Record], report_on_mr=True) -> bool:
    apex_ns_records = []
    delegation_ns_records = set()
    other_records: list[Record] = []
    for rec in records:
        if rec.type != "NS":
            other_records.append(rec)
        # We must ignore APEX NS records
        elif not rec.name or rec.name in ("", "@"):
            apex_ns_records.append(rec)
        else:
            delegation_ns_records.add(rec.name)

    invalid_records: dict[str, list[Record]] = {}
    for deleg in delegation_ns_records:
        sub_deleg = f".{deleg}"
        for rec in other_records:
            if rec.name == deleg or rec.name.endswith(sub_deleg):
                g = invalid_records.setdefault(deleg, [])
                g.append(rec)

    if not invalid_records:
        return True

    error_list = "\n".join(
        f"- {r.name} ({r.type}) => {deleg}"
        for deleg, records in invalid_records.items()
        for r in records
    )
    error_msg = f"""\
The following records are under a delegated zone (i.e. the records ends with the same value as an existing NS record)
The record is therefore not valid and must be moved to the correct zone.

{error_list}
"""
    log.error(error_msg)
    if report_on_mr:
        add_mr_comment(error_msg)
    return False


def check_duplicates(records: Iterable[Record], report_on_mr=True) -> bool:
    grouped = group(records, lambda r: r.name)
    grouped = {k: v for k, v in grouped.items() if len(v) > 1}
    if not grouped:
        return True
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
        return True
    log.warning(
        ("There are duplicate entries," "be sure that it is what you want:\n{}").format(
            "\n".join(grouped.keys())
        )
    )
    duplicates_str = "\n".join(duplicates)
    error_msg = f"""\
The following records have duplicates
Note that some records can be duplicated (e.g. A, AAAA, NS),
and some types are compatibles (e.g. A and AAAA):
{duplicates_str}
"""
    if report_on_mr:
        add_mr_comment(error_msg)
    return False


def check_records(records, raise_on_invalid=True, report_on_mr=True):
    records: Iterable[Record] = RecordList.validate_python(records)  # model_validate
    valid = True
    valid &= check_duplicates(records, report_on_mr=report_on_mr)
    valid &= check_ns_records(records, report_on_mr=report_on_mr)
    if not is_sorted(records, key=lambda x: x.name):
        # NOTE: This must not fail the pipeline. This is an additional warning
        # The error is located where the data are defined.
        log.warning("Records are not sorted, please sort them")
    if not valid and raise_on_invalid:
        raise Exception("Records are invalids. Check the logs for more information.")
    return records, valid


def sort_records(records):
    # NOTE: `sorted` is stable: https://stackoverflow.com/questions/1915376/is-pythons-sorted-function-guaranteed-to-be-stable
    # meaning: in case of equality, the order of the output is the same as the input
    yield from sorted(records, key=lambda r: (r["name"], r["type"]))
