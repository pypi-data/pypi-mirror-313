from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.exists_route_json_body_http_method import ExistsRouteJsonBodyHttpMethod

T = TypeVar("T", bound="ExistsRouteJsonBody")


@_attrs_define
class ExistsRouteJsonBody:
    """
    Attributes:
        route_path (str):
        http_method (ExistsRouteJsonBodyHttpMethod):
    """

    route_path: str
    http_method: ExistsRouteJsonBodyHttpMethod
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        route_path = self.route_path
        http_method = self.http_method.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "route_path": route_path,
                "http_method": http_method,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        route_path = d.pop("route_path")

        http_method = ExistsRouteJsonBodyHttpMethod(d.pop("http_method"))

        exists_route_json_body = cls(
            route_path=route_path,
            http_method=http_method,
        )

        exists_route_json_body.additional_properties = d
        return exists_route_json_body

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
