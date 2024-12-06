from typing import Optional, no_type_check

from django.db.models import TextField, CharField
from ninja import Schema, Router, ModelSchema, FilterSchema
from ninja.orm import create_schema
from ninja.orm.metaclass import MetaConf, ResolverMetaclass
from pydantic import BaseModel, Field


def camel_case(text: str | None) -> str:
    """Convert a string to camelCase."""
    words = (text or "").split("_")
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


class AliasMixin(BaseModel):
    """Base schema to support camelCase."""

    class Config(Schema.Config):
        alias_generator = camel_case
        populate_by_name = True


class InMeta(ModelSchema.Config):
    """Base schema for incoming data."""

    fields = "__all__"
    fields_optional = "__all__"


class OutMeta(ModelSchema.Config):
    """Base schema for outgoing data."""

    fields = "__all__"


class AliasRouter(Router):
    """Alias router to support camelCase."""

    def api_operation(self, *a, **kw):
        """Allow alias for all endpoints."""
        kw["by_alias"] = True
        return super().api_operation(*a, **kw)


_is_filter_model_schema_class_defined = False


class FilterModelSchemaMetaclass(ResolverMetaclass):
    @staticmethod
    def _collect_custom_fields(meta_conf: MetaConf, namespace: dict):
        custom_fields = {}
        for model_field in meta_conf.model._meta.fields:
            if isinstance(model_field, TextField) or isinstance(model_field, CharField):
                field = Field(
                    None,
                    description="Filter if entry contains",
                    q=f"{model_field.name}__icontains",
                )  # noqa
            else:
                field = Field(None, description="Filter if entry is exact")
            custom_fields[model_field.name] = (model_field.name, Optional[str], field)

        annotations = namespace.get("__annotations__", {})
        for attr_name, type_hint in annotations.items():
            if attr_name.startswith("_"):
                continue
            default = namespace.get(attr_name, ...)
            custom_fields[attr_name] = (attr_name, type_hint, default)
        return custom_fields

    @no_type_check
    def __new__(
        mcs,
        name: str,
        bases: tuple,
        namespace: dict,
        **kwargs,
    ):
        cls = super().__new__(
            mcs,
            name,
            bases,
            namespace,
            **kwargs,
        )
        for base in reversed(bases):
            if (
                _is_filter_model_schema_class_defined
                and issubclass(base, FilterModelSchema)
                and base == FilterModelSchema
            ):
                meta_conf = MetaConf.from_schema_class(name, namespace)
                custom_fields = mcs._collect_custom_fields(meta_conf, namespace)

                print(meta_conf)
                model_schema = create_schema(
                    meta_conf.model,
                    name=name,
                    fields=meta_conf.fields,
                    exclude=meta_conf.exclude,
                    optional_fields=meta_conf.fields_optional,
                    custom_fields=custom_fields.values(),
                    base_class=cls,
                )
                model_schema.__doc__ = cls.__doc__
                return model_schema
        return cls


class FilterModelSchema(FilterSchema, metaclass=FilterModelSchemaMetaclass):
    pass


_is_filter_model_schema_class_defined = True  # noqa
