import json
import os
from ..utils import copy_text_resource

class BaseRepo:
    _repo: dict[str, object]

    # To be defined in subclasses
    _filename: str
    _key_field: str
    _model_cls: type
    _default_provided: bool = False

    def __init__(self):
        self._repo = {}
        os.makedirs(os.path.dirname(self._filename), exist_ok=True)
        if not os.path.exists(self._filename):
            if self._default_provided:
                copy_text_resource(
                    resource=os.path.basename(self._filename),
                    dest_path=self._filename
                )
            else:
                self._persist()
        self._reload()

    def _reload(self):
        self._repo = {}
        with open(self._filename, "r") as f:
            data = json.load(f)
            for item in data:
                key = item[self._key_field]
                self._repo[key] = self._model_cls(**item)

    def _persist(self):
        with open(self._filename, "w") as f:
            data = [model.model_dump() for model in self._repo.values()]
            json.dump(data, f)