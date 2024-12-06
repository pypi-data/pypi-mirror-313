import json
import typing as t

from pydantic import BaseModel


def short_write(filename, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_from_file(filename: str, base_class: t.Type[BaseModel]):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        return base_class.model_validate(data)
