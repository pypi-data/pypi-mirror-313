from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_type import LogType






T = TypeVar("T", bound="ReportLogInput")


@_attrs_define
class ReportLogInput:
    """ 
        Attributes:
            checksum (str):
            file_name (str):
            file_size (int):
            log_type (LogType):
     """

    checksum: str
    file_name: str
    file_size: int
    log_type: LogType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        checksum = self.checksum

        file_name = self.file_name

        file_size = self.file_size

        log_type = self.log_type.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "checksum": checksum,
            "fileName": file_name,
            "fileSize": file_size,
            "logType": log_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        checksum = d.pop("checksum")

        file_name = d.pop("fileName")

        file_size = d.pop("fileSize")

        log_type = LogType(d.pop("logType"))




        report_log_input = cls(
            checksum=checksum,
            file_name=file_name,
            file_size=file_size,
            log_type=log_type,
        )


        report_log_input.additional_properties = d
        return report_log_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
