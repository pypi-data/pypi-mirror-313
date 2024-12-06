from pathlib import Path as _p


class UniqueChecker(object):
    def __init__(self):
        self.path_dict = {}

    def add(self, path: _p):
        if path in self.path_dict:
            raise ValueError(f"{path} already exists")
        self.path_dict[path] = True