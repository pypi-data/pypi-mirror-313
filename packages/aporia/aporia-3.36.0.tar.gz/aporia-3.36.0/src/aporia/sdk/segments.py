from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client


def _format_number(n):
    # This is to mimic the following JS code:
    # n.toLocaleString(undefined, {maximumFractionDigits: 4})
    # It's possible different locales will display it differently in JS, but using n
    # instead of , in the format string lead to exponent view, which is incorrect.
    # Reference: https://stackoverflow.com/questions/1823058/how-to-print-a-number-using-commas-as-thousands-separators
    rounded_number = round(n, ndigits=4)
    return f"{rounded_number:,}"


def _format_string(n):
    # This is to mimic String in JS code.
    if isinstance(n, bool):
        return str(n).lower()
    return str(n)


def _get_numeric_buckets(segment_data: Dict) -> List[Dict]:
    values = segment_data["values"]
    result = []
    for i in range(len(values) - 1):
        value = values[i]
        next_value = values[i + 1]
        name = f"{_format_number(value)} - {_format_number(next_value)}"
        result.append({"value": value, "nextValue": next_value, "name": name})

    return result


def _get_non_numeric_buckets(segment_data: Dict) -> List[Dict]:
    values = segment_data["values"]
    return [{"value": value, "name": _format_string(value)} for value in values]


class Segment(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)
        self.extended_data = None

    def __update_members(self, data: Dict):
        self.raw_data = data
        self.id = data["id"]
        self.name = data["name"]
        self.field_name = data["field_name"]
        self.values = data["values"]
        self.terms = data["terms_values"]

    def __update_extended_data(self):
        response = self.client.send_request(
            f"/data-segments/{self.id}",
            "GET",
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        self.client.assert_response(response)
        self.extended_data = response.json()

    def get_extended_data(self) -> Dict:
        if self.extended_data is None:
            self.__update_extended_data()
        return self.extended_data

    def get_widget_values(self) -> List[Any]:
        if self.extended_data is None:
            self.__update_extended_data()

        if (
            self.extended_data["is_custom_segment"]
            or self.extended_data["field"]["type"] != "numeric"
        ):
            return self.values
        return self.values[:-1]

    def to_widget(self) -> Dict:
        if self.extended_data is None:
            self.__update_extended_data()

        segment_data = {
            "id": self.id,
            "name": self.name,
            "createdAt": self.raw_data["created_at"],
            "isGlobalFilter": self.extended_data["create_composite_segments"],
            "values": self.extended_data["values"],
        }

        if self.extended_data["is_custom_segment"]:
            segment_data["type"] = "custom"
            segment_data["termsValues"] = self.extended_data["terms_values"]
        else:
            segment_data["type"] = "auto"
            segment_data["fieldId"] = self.extended_data["field"]["id"]
            segment_data["fieldType"] = self.extended_data["field"]["type"]
            if segment_data["fieldType"] == "numeric":
                segment_data["buckets"] = _get_numeric_buckets(self.extended_data)

        if "buckets" not in segment_data:
            segment_data["buckets"] = _get_non_numeric_buckets(self.extended_data)

        return segment_data

    @classmethod
    def get_all(
        cls, client: Client, model_id: Optional[str] = None, manual_only: bool = True
    ) -> List["Segment"]:
        url_params = {}
        if manual_only:
            url_params["is_manually_created"] = "true"
        if model_id is not None:
            url_params["model_id"] = model_id
        encoded_url_params = urlencode(url_params)
        response = client.send_request(
            f"/data-segments{f'?{encoded_url_params}' if len(url_params) > 0 else f''}",
            "GET",
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        model_id: str,
        field_name: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
        is_global_filter: bool = False,
    ) -> "Segment":
        segment_data = {}
        if terms is not None:
            segment_data["terms_values"] = terms
        else:
            segment_data["field_name"] = field_name
            segment_data["values"] = values
        segment_data["is_global_filter"] = is_global_filter
        response = client.send_request(
            "/data-segments",
            "POST",
            {"name": name, "model_id": model_id, **segment_data},
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Segment":
        response = client.send_request(f"/data-segments/{id}", "GET")
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(
        self,
        name: Optional[str] = None,
        field_name: Optional[str] = None,
        values: Optional[Union[List[str], List[Union[float, int]]]] = None,
        terms: Optional[List[Tuple[str, str]]] = None,
        is_global_filter: Optional[bool] = None,
        **kwargs,
    ):
        args = {}
        if name is not None:
            args["name"] = name
        if field_name is not None:
            args["field_name"] = field_name
        if values is not None:
            args["values"] = values
        if terms is not None:
            args["terms_values"] = terms
        if is_global_filter is not None:
            args["is_global_filter"] = is_global_filter
        response = self.client.send_request(
            f"/data-segments/{self.id}",
            "PUT",
            args,
        )
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/data-segments/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/data-segments/{id}", "DELETE")
        client.assert_response(response)
