from typing import TYPE_CHECKING, Any, Optional, Union, cast

from pydantic import BaseModel

if TYPE_CHECKING:
    from weba import Tag


from bs4.element import Tag as Bs4Tag


class SetValuesMixin:
    def set_values(self, data: dict[str, Any], tag: Optional["Tag"] = None) -> "Tag":
        tag = tag or self  # pyright: ignore[reportAssignmentType]

        flattened_data = flatten_to_values(data)

        elements = cast(list["Tag"], tag.find_all(attrs={"set-values": True}) or [])  # type: ignore

        decompose_list: list["Tag"] = []

        for element in elements:
            values = element.attrs.pop("set-values").split(",")

            for value in values:
                key, attr = (value.strip().split("#") + ["string"])[:2]

                if value := flattened_data.get(key):
                    if attr == "string":
                        if isinstance(value, Bs4Tag):
                            element.clear()
                            element.append(value)
                        else:
                            element.string = str(value)
                    else:
                        element.attrs[attr] = str(value)
                # NOTE: Appending to a decompose_list ensures that elements are only decomposed once,
                # as they can appear multiples due to splitting by
                elif element not in decompose_list:
                    decompose_list.append(element)

        [element.decompose() for element in decompose_list]

        return cast("Tag", tag)


def flatten_to_values(data: Union[dict[str, Any], BaseModel], parent_key: str = "", sep: str = "[") -> dict[str, Any]:
    items: dict[str, Any] = {}

    if isinstance(data, BaseModel):
        data = data.model_dump()  # Use model_dump() for Pydantic models

    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}]" if parent_key else k

        if isinstance(v, dict):
            items.update(flatten_to_values(cast(Any, v), new_key, sep=sep))
        elif isinstance(v, BaseModel):
            items.update(flatten_to_values(v.model_dump(), new_key, sep=sep))  # Use model_dump() here as well
        elif isinstance(v, list):
            for i, item in enumerate(cast(list[Any | dict[str, Any]], v)):
                array_key = f"{new_key}{sep}{i}]"

                if isinstance(item, (dict, BaseModel)):
                    items.update(flatten_to_values(item, array_key, sep=sep))
                else:
                    items[array_key] = item
        else:
            items[new_key] = v

    return items
