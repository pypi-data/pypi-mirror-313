from typing import AbstractSet, Any, Iterable, Mapping, Sequence

from marshmallow import Schema


class GenericSchema(Schema):

    def dump(self, obj: Any, *, many: bool | None = None):
        many = self.many if many is None else bool(many)
        if many:
            return [vars(item) for item in obj]
        return vars(obj)

    def load(self, data: Mapping[str, Any] | Iterable[Mapping[str, Any]], *, many: bool | None = None, partial: bool | Sequence[str] | AbstractSet[str] | None = None, unknown: str | None = None, instance: Any | None = None):
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            return instance
        return super().load(data, many=many, partial=partial, unknown=unknown)
