from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic._internal import _model_construction  # noqa
from pydantic.fields import FieldInfo  # noqa
from pydantic_core import PydanticUndefined


class BaseModelMetaclass(_model_construction.ModelMetaclass):

    def __new__(
            mcs,
            cls_name: str,
            bases: tuple[type[Any], ...],
            namespace: dict[str, Any],
            **kwargs: Any,
    ) -> type:
        namespace = mcs.update_namespace(namespace)
        return super().__new__(mcs, cls_name, bases, namespace, **kwargs)

    @staticmethod
    def update_namespace(namespace: dict[str, Any]) -> dict[str, Any]:
        if '__annotations__' in namespace:
            namespace['__annotations__'] = {k: v | None for k, v in namespace['__annotations__'].items()}
            for k, v in namespace['__annotations__'].items():
                namespace['__annotations__'][k] = v | None
                if k not in namespace:
                    namespace[k] = None
                elif isinstance(namespace[k], FieldInfo) and namespace[k].default is PydanticUndefined:
                    namespace[k].default = None
        return namespace


class NullableBaseModel(BaseModel, metaclass=BaseModelMetaclass):
    model_config = ConfigDict(extra='allow')
    pass


if __name__ == '__main__':
    pass
