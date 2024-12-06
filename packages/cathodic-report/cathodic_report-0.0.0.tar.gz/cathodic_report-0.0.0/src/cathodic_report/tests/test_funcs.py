import datetime
import pathlib as pl

from cathodic_report import funcs


def test_get_date_name():
    now = datetime.datetime.now()
    assert funcs.get_date_name(pl.Path("test.txt")) == pl.Path(f"{now.year}-{now.month}-{now.day}/test.txt")
    assert funcs.get_date_name(pl.Path(".")) == pl.Path(f"{now.year}-{now.month}-{now.day}")
