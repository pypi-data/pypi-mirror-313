from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.triggered_via import TriggeredVia
from typing import Union
from ..types import UNSET, Unset






T = TypeVar("T", bound="CreateBuildForSystemInput")


@_attrs_define
class CreateBuildForSystemInput:
    """ 
        Attributes:
            branch_id (str):
            image_uri (str):
            version (str):
            associated_account (Union[Unset, str]):
            description (Union[Unset, str]):
            triggered_via (Union[Unset, TriggeredVia]):
     """

    branch_id: str
    image_uri: str
    version: str
    associated_account: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    triggered_via: Union[Unset, TriggeredVia] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        branch_id = self.branch_id

        image_uri = self.image_uri

        version = self.version

        associated_account = self.associated_account

        description = self.description

        triggered_via: Union[Unset, str] = UNSET
        if not isinstance(self.triggered_via, Unset):
            triggered_via = self.triggered_via.value



        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "branchID": branch_id,
            "imageUri": image_uri,
            "version": version,
        })
        if associated_account is not UNSET:
            field_dict["associatedAccount"] = associated_account
        if description is not UNSET:
            field_dict["description"] = description
        if triggered_via is not UNSET:
            field_dict["triggeredVia"] = triggered_via

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        branch_id = d.pop("branchID")

        image_uri = d.pop("imageUri")

        version = d.pop("version")

        associated_account = d.pop("associatedAccount", UNSET)

        description = d.pop("description", UNSET)

        _triggered_via = d.pop("triggeredVia", UNSET)
        triggered_via: Union[Unset, TriggeredVia]
        if isinstance(_triggered_via,  Unset):
            triggered_via = UNSET
        else:
            triggered_via = TriggeredVia(_triggered_via)




        create_build_for_system_input = cls(
            branch_id=branch_id,
            image_uri=image_uri,
            version=version,
            associated_account=associated_account,
            description=description,
            triggered_via=triggered_via,
        )


        create_build_for_system_input.additional_properties = d
        return create_build_for_system_input

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
