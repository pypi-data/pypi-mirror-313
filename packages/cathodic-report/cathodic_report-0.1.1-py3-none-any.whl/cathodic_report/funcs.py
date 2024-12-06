import pathlib
from datetime import datetime


def get_date_name(name: pathlib.Path) -> pathlib.Path:
    """在原来名称的基础上增加日期文件夹，然后把生成的文件放在日期文件夹下"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    parent = name.parent / date_str
    parent.mkdir(parents=True, exist_ok=True)
    return parent / name.name
