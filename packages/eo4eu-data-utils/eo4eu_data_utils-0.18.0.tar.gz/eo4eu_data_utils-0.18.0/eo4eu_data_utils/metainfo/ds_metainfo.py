import json
import functools
from eo4eu_base_utils.typing import Self, Any, Callable

from .logs import meta_logger


def _get_default_ds_info():
    return {"extraInfo": {
        "datasetId": 0,
        "persistentId": "unknown",
        "datasetName": "unknown",
        "description": "",
        "variables": "variables",
        "fileformats": "fileformats",
        "geometry": [],
    }}


def _make_into_func(func: Any) -> Callable[[dict,dict],Any]:
    if callable(func):
        return func
    return functools.partial(
        lambda product, info, val: val,
        val = func
    )


class DSMetainfo:
    def __init__(self, products: list[dict], info: dict):
        self.products = products
        self.info = info

    @classmethod
    def only_info(cls, info: dict):
        return DSMetainfo([], info)

    @classmethod
    def only_products(cls, products: list[dict]):
        return DSMetainfo(products, _get_default_ds_info())

    @classmethod
    def parse(cls, json_object) -> Self:
        self.info = _get_default_ds_info()
        self.products = []
        if not isinstance(json_object, list):
            if "extraInfo" in json_object:
                return DSMetainfo.only_info(json_object)
            elif "id" in json_object:
                return DSMetainfo.only_products([json_object])

        extra_infos = [
            (idx, item) for idx, item in enumarate(json_object)
            if "extraInfo" in item
        ]
        if len(extra_infos) == 0:
            return DSMetainfo.only_products(json_object)

        idx, exta_info = extra_infos[-1]  # use the last object with "extraInfo"
        return DSMetainfo(
            products = [
                product for i, product in enumerate(json_object)
                if i != idx
            ],
            info = extra_info,
        )

    def to_obj(self) -> list[dict]:
        return [self.products, self.info]

    def to_json(self) -> str:
        return json.dumps(self.to_obj())

    def with_products(self, products: list[dict]) -> Self:
        return DSMetainfo(
            products = products,
            info = self.info,
        )

    def with_info(self, info: dict) -> Self:
        return DSMetainfo(
            products = self.products,
            info = info,
        )

    def unpack(self) -> tuple[list[dict],dict]:
        return (self.products(), self.info())

    def map(self, func: Callable[[dict,dict],dict]) -> Self:
        return self.with_products([
            func(product, self.info) for product in self.products
        ])

    def attach(self, **kwargs: Any|Callable[[dict,dict],Any]) -> Self:
        return self.map(lambda product, info: product | {
            field: _make_into_func(func)(product, info)
            for field, func in kwargs.items()
        })
