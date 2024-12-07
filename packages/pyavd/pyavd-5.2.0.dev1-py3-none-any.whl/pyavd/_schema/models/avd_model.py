# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import TYPE_CHECKING, Any, ClassVar, Literal

from pyavd._schema.coerce_type import coerce_type
from pyavd._utils import Undefined, UndefinedType, merge

from .avd_base import AvdBase
from .avd_indexed_list import AvdIndexedList

if TYPE_CHECKING:
    from typing_extensions import Self

    from .type_vars import T_AvdModel


class AvdModel(AvdBase):
    """Base class used for schema-based data classes holding dictionaries loaded from AVD inputs."""

    _allow_other_keys: ClassVar[bool] = False
    """Attribute telling if this class should fail or ignore unknown keys found during loading in _from_dict()."""
    _fields: ClassVar[dict[str, dict]]
    """
    Metadata serving as a shortcut for knowing the expected type of each field and default value.
    This is used instead of inspecting the type-hints to improve performance significantly.
    """
    _field_to_key_map: ClassVar[dict[str, str]] = {}
    """Map of field name to original dict key. Used when fields have the field_ prefix to get the original key."""
    _key_to_field_map: ClassVar[dict[str, str]] = {}
    """Map of dict key to field name. Used when the key is names with a reserved keyword or mixed case. E.g. `Vxlan1` or `as`."""

    @classmethod
    def _load(cls, data: Mapping) -> Self:
        """Returns a new instance loaded with the data from the given dict."""
        return cls._from_dict(data)

    @classmethod
    def _from_dict(cls: type[T_AvdModel], data: Mapping, keep_extra_keys: bool = False) -> T_AvdModel:
        """
        Returns a new instance loaded with the data from the given dict.

        TODO: AVD6.0.0 remove the keep_extra_keys option so we no longer support custom keys without _ in structured config.
        """
        if not isinstance(data, Mapping):
            msg = f"Expecting 'data' as a 'Mapping' when loading data into '{cls.__name__}'. Got '{type(data)}"
            raise TypeError(msg)

        has_custom_data = "_custom_data" in cls._fields
        cls_args = {}

        for key in data:
            if not (field := cls._get_field_name(key)):
                if keep_extra_keys or (has_custom_data and str(key).startswith("_")):
                    cls_args.setdefault("_custom_data", {})[key] = data[key]
                    continue

                if cls._allow_other_keys:
                    # Ignore unknown keys.
                    continue

                msg = f"Invalid key '{key}'. Not available on '{cls.__name__}'."
                raise KeyError(msg)

            cls_args[field] = coerce_type(data[key], cls._fields[field]["type"])

        return cls(**cls_args)

    @classmethod
    def _get_field_name(cls, key: str) -> str | None:
        """Returns the field name for the given key. Returns None if the key is not matching a valid field."""
        field_name = cls._key_to_field_map.get(key, key)
        return field_name if field_name in cls._fields else None

    @classmethod
    def _get_field_default_value(cls, name: str) -> Any:
        """
        Returns the default value for a field.

        We check for a default value in the _fields information and if something is there we return that.
        - For dicts, AvdModel and lists of AvdModels subclasses the default value is a callable to generate a new instance to avoid reusing a mutable object.
        - For lists of simple types like 'list[str]' the default value is a list that is copied to avoid reusing a mutable object.
        - For other types, which are immutable, the default value is taken directly.

        If there is no default value in the field info, we return the default-default depending on type.
        - For lists and dicts we return new empty list / dict.
        - For AvdModel subclasses we return a new empty instance of the class.
        - For other types we return None.
        """
        if name not in cls._fields:
            msg = f"'{cls.__name__}' object has no attribute '{name}'"
            raise AttributeError(msg)
        field_info = cls._fields[name]
        field_type: type = field_info["type"]

        if issubclass(field_type, AvdBase) or field_type is dict:
            return default_function(field_type) if (default_function := field_info.get("default")) else field_type()

        return field_info.get("default")

    def __init__(self, **kwargs: Any) -> None:
        """
        Runtime init without specific kwargs and type hints.

        Only walking the given kwargs improves performance compared to having named kwargs.

        This method is typically overridden when TYPE_HINTING is True, to provider proper suggestions and type hints for the arguments.
        """
        [setattr(self, arg, arg_value) for arg, arg_value in kwargs.items() if arg_value is not Undefined]

    def __getattr__(self, name: str) -> Any:
        """
        Resolves the default value for a field, set the default value on the attribute and return the value.

        We only get here if the attribute is not set already, and next call will skip this since the attribute is set.
        """
        if name not in self._fields:
            msg = f"'{type(self).__name__}' object has no attribute '{name}'"
            raise AttributeError(msg)

        default_value = self._get_field_default_value(name)
        setattr(self, name, default_value)
        return default_value

    def _get_defined_attr(self, name: str) -> Any | UndefinedType:
        """
        Get attribute or Undefined.

        Avoids the overridden __getattr__ to avoid default values.
        """
        if name not in self._fields:
            msg = f"'{type(self).__name__}' object has no attribute '{name}'"
            raise AttributeError(msg)
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return Undefined

    def __repr__(self) -> str:
        """Returns a repr with all the fields that are set including any nested models."""
        cls_name = self.__class__.__name__
        attrs = [f"{key}={getattr(self, key)!r}" for key in self._fields if self._get_defined_attr(key) is not Undefined]
        return f"<{cls_name}({', '.join(attrs)})>"

    def __bool__(self) -> bool:
        """
        Boolean check on the class to quickly determine if any parameter is set.

        Note that a falsy value will still make this True.

        The check ignores the default values and is performed recursively on any nested models.
        """
        return any(
            # False if item is Undefined
            (value := self._get_defined_attr(field)) is not Undefined
            and
            # False if it is AVD class with a falsy value
            # True otherwise
            not (isinstance(value, AvdBase) and not value)
            for field in self._fields
        )

    def _as_dict(self, include_default_values: bool = False, strip_values: tuple = (None, [], {})) -> dict:
        """
        Returns a dict with all the data from this model and any nested models.

        Filtered for nested None, {} and [] values.
        """
        as_dict = {}
        for field, field_info in self._fields.items() or ():
            if (value := self._get_defined_attr(field)) is Undefined:
                if not include_default_values:
                    continue

                value = self._get_field_default_value(field)

            if field == "_custom_data" and isinstance(value, dict) and value:
                as_dict.update(value)
                continue

            # Removing field_ prefix if needed.
            key = self._field_to_key_map.get(field, field)

            if issubclass(field_info["type"], AvdBase) and isinstance(value, AvdBase):
                value = value._dump(include_default_values=include_default_values, strip_values=strip_values)

            if value in strip_values:
                continue

            as_dict[key] = value

        return as_dict

    def _dump(self, include_default_values: bool = False, strip_values: tuple = (None, [], {})) -> dict:
        return self._as_dict(include_default_values=include_default_values, strip_values=strip_values)

    def _get(self, name: str, default: Any = None) -> Any:
        """
        Behave like dict.get() to get a field value only if set.

        If the field balue is not set, this will not insert a default schema values but will instead return the given 'default' value (or None).
        """
        if (value := self._get_defined_attr(name)) is Undefined:
            return default
        return value

    def _update(self, other: Self) -> None:
        """Update instance by shallow merging the other instance in."""
        cls = type(self)
        if not isinstance(other, cls):
            msg = f"Unable to merge type '{type(other)}' into '{cls}'"
            raise TypeError(msg)

        for field in cls._fields:
            if new_value := other._get_defined_attr(field) is Undefined:
                continue
            old_value = self._get_defined_attr(field)
            if old_value == new_value:
                continue
            setattr(self, field, new_value)

    def _deepmerge(self, other: Self, list_merge: Literal["append", "replace"] = "append") -> None:
        """
        Update instance by deepmerging the other instance in.

        Args:
            other: The other instance of the same type to merge on this instance.
            list_merge: Merge strategy used on any nested lists.
                - "append" will first try to deep merge on the primary key, and if not found it will append non-existing items.
                - "replace" will replace the full list.
        """
        cls = type(self)
        if not isinstance(other, cls):
            msg = f"Unable to merge type '{type(other)}' into '{cls}'"
            raise TypeError(msg)

        for field, field_info in cls._fields.items():
            if (new_value := other._get_defined_attr(field)) is Undefined:
                continue
            old_value = self._get_defined_attr(field)
            if old_value == new_value:
                continue

            if not isinstance(old_value, type(new_value)):
                # Different type so we can just replace
                setattr(self, field, deepcopy(new_value))
                continue

            # Merge new value
            field_type = field_info["type"]
            if issubclass(field_type, AvdBase) and isinstance(old_value, field_type):
                # Merge in to the existing object
                old_value._deepmerge(new_value, list_merge=list_merge)
                continue

            if field_type is dict:
                # In-place deepmerge in to the existing dict without schema.
                # Deepcopying since merge() does not copy.
                merge(old_value, deepcopy(new_value), list_merge=list_merge)
                continue

            setattr(self, field, new_value)

    def _inherit(self, other: Self) -> None:
        """Update unset fields on this instance with fields from other instance. No merging."""
        cls = type(self)
        if not isinstance(other, cls):
            msg = f"Unable to inherit from type '{type(other)}' into '{cls}'"
            raise TypeError(msg)

        for field in cls._fields:
            if self._get_defined_attr(field) is not Undefined:
                continue
            if (new_value := other._get_defined_attr(field)) is Undefined:
                continue

            setattr(self, field, deepcopy(new_value))

    def _deepinherit(self, other: Self) -> None:
        """Update instance by recursively inheriting unset fields from other instance. Lists are not merged."""
        cls = type(self)
        if not isinstance(other, cls):
            msg = f"Unable to inherit from type '{type(other)}' into '{cls}'"
            raise TypeError(msg)

        for field, field_info in cls._fields.items():
            if (new_value := other._get_defined_attr(field)) is Undefined:
                continue
            old_value = self._get_defined_attr(field)
            if old_value == new_value:
                continue

            # Inherit the field only if the old value is Undefined.
            if old_value is Undefined:
                setattr(self, field, deepcopy(new_value))
                continue

            # Merge new value if it is a class with inheritance support.
            field_type = field_info["type"]
            if issubclass(field_type, (AvdModel, AvdIndexedList)) and isinstance(old_value, field_type):
                # Inherit into the existing object.
                old_value._deepinherit(new_value)
                continue

            if field_type is dict:
                # In-place deepmerge in to the existing dict without schema.
                # Deepcopying since merge() does not copy.
                merge(old_value, deepcopy(new_value), list_merge="replace")

    def _deepinherited(self, other: Self) -> Self:
        """Return new instance with the result of recursively inheriting unset fields from other instance. Lists are not merged."""
        new_instance = deepcopy(self)
        new_instance._deepinherit(other=other)
        return new_instance

    def _cast_as(self, new_type: type[T_AvdModel], ignore_extra_keys: bool = False) -> T_AvdModel:
        """
        Recast a class instance as another AvdModel subclass if they are compatible.

        The classes are compatible if the fields of the new class is a superset of the current class.
        Unset fields are ignored when evaluating compatibility.

        Useful when inheriting from profiles.
        """
        cls = type(self)
        if not issubclass(new_type, AvdModel):
            msg = f"Unable to cast '{cls}' as type '{new_type}' since '{new_type}' is not an AvdModel subclass."
            raise TypeError(msg)

        new_args = {}
        for field, field_info in cls._fields.items():
            if (value := self._get_defined_attr(field)) is Undefined:
                continue
            if field not in new_type._fields:
                if ignore_extra_keys:
                    continue
                msg = f"Unable to cast '{cls}' as type '{new_type}' since the field '{field}' is missing from the new class. "
                raise TypeError(msg)
            if field_info != new_type._fields[field]:
                if issubclass(field_info["type"], (AvdBase)) and isinstance(value, (AvdBase)):
                    # TODO: Consider using the TypeError we raise below to ensure we know the outer type.
                    # TODO: with suppress(TypeError):
                    new_args[field] = value._cast_as(new_type._fields[field]["type"], ignore_extra_keys=ignore_extra_keys)
                    continue

                msg = f"Unable to cast '{cls}' as type '{new_type}' since the field '{field}' is incompatible. Value {value}"
                raise TypeError(msg)

            new_args[field] = value
            continue

        return new_type(**new_args)
