from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Type, Annotated, get_origin
from pydantic.fields import FieldInfo
from tortoise import Model
from tortoise.queryset import QuerySet
from pydantic import BaseModel
from tortoise_filters.filter_fields import BaseFieldFilter, BaseRangeFilter


class Dependencies(BaseModel):

    @classmethod
    def add_fields(cls, **field_definitions: Any):
        new_fields: Dict[str, FieldInfo] = {}
        new_annotations: Dict[str, Optional[type]] = {}

        for f_name, f_def in field_definitions.items():
            if isinstance(f_def, tuple):
                try:
                    f_annotation, f_value = f_def
                except ValueError as e:
                    raise Exception(
                        'field definitions should either be a tuple of (<type>, <default>) or just a '
                        'default value, unfortunately this means tuples as '
                        'default values are not allowed'
                    ) from e
            else:
                f_annotation, f_value = None, f_def

            if f_annotation:
                new_annotations[f_name] = Optional[f_annotation]

            if get_origin(f_annotation) is Annotated:
                new_fields[f_name] = FieldInfo(annotation=f_annotation, default=None)
            else:
                new_fields[f_name] = FieldInfo(annotation=Optional[f_annotation], default=None)
        cls.model_fields.update(new_fields)
        cls.model_rebuild(force=True)


def create_dynamic_class(name) -> Type[Dependencies]:
    return type(name, (Dependencies,), {'greet': lambda self: "DynamicClass"})


class BaseFilterSet(ABC):
    model = None
    fields: List[str] = None

    def __init__(self, *args, **kwargs):
        pass

    async def get_queryset(self):
        return self.model.all()

    @staticmethod
    def check_fields_appearance(attr, model: Model):
        filter_fields = [value.field_name for key, value in attr.items() if isinstance(value, BaseFieldFilter)]
        model_fields = [field.model_field_name for field in model._meta.fields_map.values()]
        for field_name in filter_fields:
            if field_name not in model_fields:
                raise Exception("this field does not belong to model")

    @classmethod
    def to_dependencies(cls) -> Type[Dependencies]:
        DynamicClass = create_dynamic_class(name=cls.__name__ + "Dependencies")
        attributes = cls.__dict__
        BaseFilterSet.check_fields_appearance(attributes, cls.model)
        for key, value in attributes.items():
            if isinstance(value, BaseFieldFilter):
                if isinstance(value, BaseRangeFilter):
                    print(value, value.__annotations__)
                    dep = {}
                    value_min = (value.__annotations__.get('value_min'), None)
                    value_max = (value.__annotations__.get('value_max'), None)

                    if value_min is not None:
                        dep[f'{key}_min'] = value_min
                    if value_max is not None:
                        dep[f'{key}_max'] = value_max

                    DynamicClass.add_fields(**dep)
                else:
                    print(value, value.__annotations__)
                    dep = {}
                    # print(value.__annotations__)
                    dep[key] = (value.__annotations__.get('value'), None)
                    DynamicClass.add_fields(**dep)

        return DynamicClass

    @abstractmethod
    def filter_queryset(self):
        raise NotImplementedError


class FilterSet(BaseFilterSet):

    #todo: add processing for range filters

    def __init__(self, query_params: Dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_params = query_params

    async def filter_queryset(self) -> QuerySet[Model]:
        attributes = self.__class__.__dict__.copy()
        self.queryset = await self.get_queryset()

        for key, value in list(attributes.items()):
            if isinstance(value, BaseRangeFilter):
                attributes.pop(key)
                attributes[f'{key}_min'] = value
                attributes[f'{key}_max'] = value

        for key, value in list(attributes.items()):
            if isinstance(value, BaseFieldFilter):
                if key in self.query_params:
                    value.value = self.query_params[key]
                    self.queryset = await value.filter_queryset(self.queryset, value.value)

        return self.queryset
