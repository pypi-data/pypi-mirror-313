from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateBuildForBranchInput")


@_attrs_define
class CreateBuildForBranchInput:
    """ 
        Attributes:
            image_uri (str):
            system_id (str):
            version (str):
            associated_account (Union[Unset, str]):
            description (Union[Unset, str]):
     """

    image_uri: str
    system_id: str
    version: str
    associated_account: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        image_uri = self.image_uri

        system_id = self.system_id

        version = self.version

        associated_account = self.associated_account

        description = self.description


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "imageUri": image_uri,
            "systemID": system_id,
            "version": version,
        })
        if associated_account is not UNSET:
            field_dict["associatedAccount"] = associated_account
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        image_uri = d.pop("imageUri")

        system_id = d.pop("systemID")

        version = d.pop("version")

        associated_account = d.pop("associatedAccount", UNSET)

        description = d.pop("description", UNSET)

        create_build_for_branch_input = cls(
            image_uri=image_uri,
            system_id=system_id,
            version=version,
            associated_account=associated_account,
            description=description,
        )


        create_build_for_branch_input.additional_properties = d
        return create_build_for_branch_input

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
