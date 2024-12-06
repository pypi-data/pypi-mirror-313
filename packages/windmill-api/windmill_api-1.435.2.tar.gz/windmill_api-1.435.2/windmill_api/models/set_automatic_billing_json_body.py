from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SetAutomaticBillingJsonBody")


@_attrs_define
class SetAutomaticBillingJsonBody:
    """
    Attributes:
        automatic_billing (bool):
        seats (Union[Unset, float]):
    """

    automatic_billing: bool
    seats: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        automatic_billing = self.automatic_billing
        seats = self.seats

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "automatic_billing": automatic_billing,
            }
        )
        if seats is not UNSET:
            field_dict["seats"] = seats

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        automatic_billing = d.pop("automatic_billing")

        seats = d.pop("seats", UNSET)

        set_automatic_billing_json_body = cls(
            automatic_billing=automatic_billing,
            seats=seats,
        )

        set_automatic_billing_json_body.additional_properties = d
        return set_automatic_billing_json_body

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
