from ipaddress import IPv4Address, IPv6Address
from typing import Type

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction, IntegrityError
from django.db.models import Model, QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from ninja import ModelSchema, FilterSchema, NinjaAPI


def list_all(
    source: type[Model] | type[QuerySet], filters: FilterSchema = None
) -> list[Model]:
    """List instances of the model."""
    if isinstance(source, type) and issubclass(source, Model):
        source = source.objects.all()
    return filters.filter(source) if filters else source


def get(model: Type[Model], pk: int) -> Model:
    """Get instance of the model."""
    return get_object_or_404(model, pk=pk)


def convert_ip_to_string(data: dict) -> dict[str, any]:
    """Convert any IP address fields to string format."""
    return {
        key: str(value) if isinstance(value, (IPv4Address, IPv6Address)) else value
        for key, value in data.items()
    }


def handle_many_to_many_fields(model, data: dict):
    """Extract many-to-many fields from data."""
    many_to_many_fields = {}
    for field in model._meta.many_to_many:
        if field.name in data:
            many_to_many_fields[field.name] = data.pop(field.name)
    return many_to_many_fields


def handle_foreign_keys(model, data: dict):
    """Adjust foreign key fields in data by converting related fields to IDs."""
    for field in model._meta.fields:
        if field.is_relation and field.many_to_one and field.name in data:
            if isinstance(data[field.name], dict) and "id" in data[field.name]:
                data[f"{field.name}_id"] = data.pop(field.name)["id"]
            elif isinstance(data[field.name], int):
                data[f"{field.name}_id"] = data.pop(field.name)


def handle_reverse_relations(model, data: dict):
    """Extract reverse relations from data and prepare them for update/create."""
    reverse_fields = {}
    for rel in model._meta.related_objects:
        related_name = rel.related_name
        if related_name in data:
            reverse_rel_fields = data.pop(related_name)
            rel_items = []
            for entry in reverse_rel_fields:
                entry_id = entry.pop("id", None)
                entry.pop(rel.field.name, None)
                rel_item, _ = rel.related_model.objects.update_or_create(
                    id=entry_id, defaults=entry
                )
                rel_items.append(rel_item)
            reverse_fields[related_name] = rel_items
    return reverse_fields


def create(model: Type[Model], payload: ModelSchema) -> Model:
    """Create an instance of the model with improved readability and efficiency."""
    data = payload.dict(exclude_none=True)
    data = convert_ip_to_string(data)

    many_to_many_fields = handle_many_to_many_fields(model, data)
    handle_foreign_keys(model, data)
    reverse_fields = handle_reverse_relations(model, data)

    instance = model(**data)
    instance.save()

    for field, value in many_to_many_fields.items():
        getattr(instance, field).set(value)

    for field, value in reverse_fields.items():
        getattr(instance, field).set(value)

    return instance


def update(model: Type[Model], pk: int, payload: ModelSchema) -> Model:
    """Update an instance of the specified model with the provided payload."""
    instance = get_object_or_404(model, pk=pk)

    with transaction.atomic():
        updated_data = convert_ip_to_string(payload.dict())

        many_to_many_fields = handle_many_to_many_fields(
            instance._meta.model, updated_data
        )
        foreign_key_fields = [
            field.name
            for field in instance._meta.model._meta.fields
            if field.is_relation and field.many_to_one
        ]
        reverse_relation_fields = handle_reverse_relations(
            instance._meta.model, updated_data
        )

        for field in payload.model_fields_set:
            if field in many_to_many_fields:
                getattr(instance, field).set(updated_data[field])
            elif field in foreign_key_fields:
                fk_id_field = f"{field}_id"
                if isinstance(updated_data[field], int):
                    setattr(instance, fk_id_field, updated_data[field])
                elif (
                    isinstance(updated_data[field], dict)
                    and "id" in updated_data[field]
                ):
                    setattr(instance, fk_id_field, updated_data[field]["id"])
            elif field in reverse_relation_fields:
                related_manager = getattr(instance, field)
                related_manager.set(reverse_relation_fields[field])
            else:
                setattr(instance, field, updated_data[field])

        instance.save()

    return instance


def upsert(model: Type[Model], payload: ModelSchema) -> Model:
    """Upsert instance of the model."""
    if payload.id is not None:
        instance = model.objects.get_or_create(pk=payload.id)[0]
        return update(model, instance.id, payload)
    return create(model, payload)


def delete(model: Type[Model], pk: int) -> int:
    """Delete instance of the model."""
    get_object_or_404(model, pk=pk).delete()
    return 204


def register_error_handlers(api: NinjaAPI):
    """Register error handlers."""

    @api.exception_handler(ImportError)
    def import_errors(request, exc: ImportError):
        """Handle import errors."""
        return JsonResponse(
            {"detail": [{"loc": ["database"], "msg": exc.msg}]}, status=422
        )

    @api.exception_handler(IntegrityError)
    def integrity_errors(request, exc: IntegrityError):
        """Handle integrity errors."""
        return JsonResponse(
            {"detail": [{"loc": ["database"], "msg": str(exc)}]}, status=422
        )

    @api.exception_handler(ObjectDoesNotExist)
    def not_found(request, exc: ObjectDoesNotExist):
        """Handle object not found errors."""
        return HttpResponse(exc, status=404)

    @api.exception_handler(ValidationError)
    def validation_errors(request, exc: ValidationError):
        """Handle validation errors."""
        return HttpResponse(exc, status=422)
