import os
from pydantic import RootModel

from ..utils import copy_text_resource

from ..models import BaseModel
from ..schemas import BaseSchema

class BaseRepo():
    _data: dict[str, BaseSchema]

    # To be defined in subclasses
    _filename: str
    _key_field: str
    _BaseSchema: type[BaseSchema]
    _default_provided: bool = False
    _NotFoundException: type[Exception] | None = ValueError

    def __init__(self):
        self._data = {}
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
    
    def to_model(self, item: BaseSchema) -> BaseModel:
        raise NotImplementedError()

    def __getitem__(self, key: str) -> BaseModel:
        if key not in self._data.keys():
            raise self._NotFoundException()
        return self.to_model(self._data[key])

    def save(self, item: BaseModel):
        self._data[getattr(item, self._key_field)] = self._BaseSchema.from_model(item)
        self._persist()

    def _reload(self):
        self._data = {}
        with open(self._filename, "r") as f:
            raw = f.read()
        self._data = RootModel[dict[str, self._BaseSchema]].model_validate_json(raw).root

    def _persist(self):
        model = RootModel(root=self._data)
        with open(self._filename, "w") as f:
            f.write(model.model_dump_json(indent=2))