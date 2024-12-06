from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateUserRequest")


@_attrs_define
class CreateUserRequest:
    """
    Attributes:
        email (str): Email
        password1 (str): Password1
        password2 (str): Password2
        nickname (str): Nickname
        lat (float): Lat
        lng (float): Lng
    """

    email: str
    password1: str
    password2: str
    nickname: str
    lat: float
    lng: float
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email

        password1 = self.password1

        password2 = self.password2

        nickname = self.nickname

        lat = self.lat

        lng = self.lng

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password1": password1,
                "password2": password2,
                "nickname": nickname,
                "lat": lat,
                "lng": lng,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email")

        password1 = d.pop("password1")

        password2 = d.pop("password2")

        nickname = d.pop("nickname")

        lat = d.pop("lat")

        lng = d.pop("lng")

        create_user_request = cls(
            email=email,
            password1=password1,
            password2=password2,
            nickname=nickname,
            lat=lat,
            lng=lng,
        )

        create_user_request.additional_properties = d
        return create_user_request

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
