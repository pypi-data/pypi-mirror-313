from __future__ import annotations


# Python Modules
import abc
import dataclasses
import datetime
import logging
import re
import os

from contextlib import contextmanager
from io import IOBase, StringIO

from pathlib import Path
from typing import Any, Callable, ClassVar, Iterable, Mapping, Optional, Type, TypeVar, Union, \
    get_args, \
    get_origin, get_type_hints

# 3rd Party Modules
import yaml
import yaml_include

from icontract import ensure, require
from dateutil.parser import parse as parse_date
from pydantic.dataclasses import dataclass as pydantic_dataclass
from yamlable import YamlAble

# Project Modules
from rwskit.dataclasses_ import DataclassRegistry
from rwskit.types_ import get_qualified_name

log = logging.getLogger(__name__)


T = TypeVar("T", bound="YamlConfig")
E = TypeVar("E", bound="EnvironmentConfig")
I = TypeVar("I")

TypeParser = Callable[[str], I]


# Enable include directives inside yaml files
@contextmanager
def _enable_yaml_include(path: Path):
    tags = ("!inc", "!include")
    loaders = (yaml.Loader, yaml.BaseLoader, yaml.SafeLoader, yaml.FullLoader)
    base_dir = path.parent

    for tag in tags:
        for loader in loaders:
            yaml.add_constructor(tag, yaml_include.Constructor(base_dir=base_dir), loader)

    yield

    for tag in tags:
        for loader in loaders:
            del loader.yaml_constructors[tag]


# According to the python documentation the following (commented) code should
# allow any class that uses the 'YamlConfigMeta' to automatically be viewed
# as a dataclass from the perspective of the type checker. Unless I am doing
# something wrong (very possible), it does not work for me and PyCharm
# does not detect that subclasses should be considered as dataclasses. The
# code functions correctly, but PyCharm will issue warnings about unresolved
# attributes for all subclasses and cannot provide autocompletion.
#
# However, if you annotate each individual class with @dataclass_transform
# PyCharm will recognize the class as a dataclass. This is obviously not ideal
# but better than nothing.

# @dataclass_transform(kw_only_default=True, frozen_default=True)
# class DataclassMeta(type):
#     def __new__(mcs, name, bases, namespace, **kwargs):
#         new_cls = super().__new__(name, bases, namespace, **kwargs)
#         return pydantic_dataclass(new_cls, frozen=True, kw_only=True)
#
#
# class YamlConfigMeta(DataclassMeta, type(YamlAble)):
#     pass


def config_dataclass(cls: Type[T]):
    """A decorator to convert a class to a frozen keyword only pydantic dataclass."""

    return pydantic_dataclass(cls, frozen=True, kw_only=True)


class YamlConfig(YamlAble):
    """A base class for serializable configuration objects.

    Classes that inherit from this class can easily be serialized to and from
    YAML files. Given a YAML file, the class can be reconstructed as long
    as the YAML attributes can be uniquely mapped to a subclass of
    :class:`YamlConfig`.

    Additionally, the configuration can be split across multiple files for
    better modularity using the ``!include`` directive.

    Examples
    --------
    >>> class ChildConfig(YamlConfig):
    ...     id: int
    ...     name: str
    ...     timestamp: datetime.datetime
    >>> class ParentConfig(YamlConfig):
    ...     parent_attr: str = "parent_attr_value"
    ...     child_attr:
    >>> expected_config = ParentConfig(
    ...     id=1,
    ...     child_config=ChildConfig(
    ...         id=2,
    ...         name="child_config",
    ...         timestamp=datetime.datetime.now()
    ... )
    >>> plain_yaml = '''
    ... child_config:
    ...     id: 2
    ...     name: child_config
    ...     timestamp: 2024-11-19 13:55:34.064388
    ...  id: 1
    ... '''
    >>> from_plain_yaml = YamlConfig.loads_yaml(plain_yaml)
    >>> assert from_plain_yaml == expected_config

    The ``!yamlable`` tag can be used  to explicitly tell the YAML parser
    which class to construct. The syntax is ``!yamlable/<fully_qualified_class_name>``.

    >>> tagged_yaml = '''
    ... !yamlable/my_package.my_module.ParentConfig
    ... child_config: !yamlable/my_package.my_module.ChildConfig
    ...     id: 2
    ...     name: child_config
    ...     timestamp: 2024-11-19 13:55:34.064388
    ... id: 1
    ... '''
    >>> assert YamlConfig.loads_yaml(tagged_yaml) == expected_config

    You can use the ``!include`` directive to include other YAML files.
    For example, assume you have the following two YAML files:

    .. code-block:: yaml

        # child_config.yaml

        id: 2
        name: "child_config"
        timestamp: 2024-11-19 13:55:34.064388

    .. code-block:: yaml

        # parent_config.yaml

        id: 1
        child_config: !include child_config.yaml

    You can load the parent config using ``YamlConfig.load_yaml`` as follows:

    >>> YamlConfig.load_yaml("parent_config.yaml")
    """
    # Maintain a registry of all classes that inherit from this base class.
    # Although, I don't plan to use this in a multithreaded context, it is
    # pretty easy to make it thread safe with a lock.
    __registry: ClassVar[DataclassRegistry] = DataclassRegistry()

    default_type_parsers = {
        int: int,
        float: float,
        bool: lambda x: x.lower() in ("true", "1", "t", "y", "yes"),
        str: lambda x: x,
        datetime.datetime: parse_date,
        datetime.date: lambda x: parse_date(x).date(),
    }

    @require(
        lambda self: dataclasses.is_dataclass(self),
        "The class must be a dataclass."
    )
    def __init__(self):
        pass

    def __init_subclass__(cls: Type[YamlConfig], **kwargs: Any):
        """Initialize subclasses to make them suitable configuration objects.

        * Automatically assign the ``__yaml_tag_suffix__`` using the fully
          qualified class name.
        * Convert the class to a ``pydantic.dataclasses.dataclass`` that has
          ``frozen=True`` and ``kw_only=True``.

        Parameters
        ----------
        kwargs : Any
        """
        super().__init_subclass__(**kwargs)

        cls.__yaml_tag_suffix__ = get_qualified_name(cls)

        # Add the subclass to the registry so we can dynamically load the class
        # without having to import it first.
        YamlConfig.__registry.register(cls)  # noqa

    @classmethod
    def get_registered_classes(cls) -> set[Type[YamlConfig]]:
        """Get the set of classes currently registered as configuration objects.

        Returns
        -------
        set[Type[YamlConfig]]
            The set of registered yaml config classes.

        """
        return set(cls.__registry)

    def dumps_plain_yaml(self) -> str:
        """
        Represent the class as plain YAML without any tags.

        .. note::
            It may not be possible to reconstruct the python object from this
            string.

        Returns
        -------
        str
            The object as plain YAML without any tags.
        """

        def _dataclass_to_dict(obj: Any):
            if dataclasses.is_dataclass(obj):
                return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
            elif isinstance(obj, str):
                return obj
            elif isinstance(obj, Mapping):
                return {k: _dataclass_to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, Iterable):
                return [_dataclass_to_dict(v) for v in obj]
            else:
                return obj

        def _transform_sets_to_lists(obj: Any):
            if isinstance(obj, set):
                return [_transform_sets_to_lists(e) for e in obj]
            elif isinstance(obj, Mapping):
                return {k: _transform_sets_to_lists(v) for k, v in obj.items()}
            elif isinstance(obj, str):
                return obj
            elif isinstance(obj, Iterable):
                return [_transform_sets_to_lists(v) for v in obj]
            else:
                return obj

        d = _transform_sets_to_lists(_dataclass_to_dict(self))

        return yaml.safe_dump(d)

    @classmethod
    @require(
        lambda file_path_or_stream: isinstance(file_path_or_stream, (str, Path, IOBase, StringIO)),
        "'file_path_or_stream' must be a string, pathlib.Path, IOBase, or StringIO object."
    )
    def load_yaml(
            cls: Type[T],
            file_path_or_stream: str | Path | IOBase | StringIO,
            safe: bool = True
    ) -> T:
        raw_config = cls._load_raw_yaml(file_path_or_stream, safe)

        # If the deserialized object is an instance of the loader class then
        # we can simply return the object (i.e., it contained all the tags
        # necessary to reconstruct the config).
        if isinstance(raw_config, cls):
            return raw_config

        # Since a config file represents a data class the top level
        # object of a plain yaml config must be a dictionary (i.e., the
        # attributes of the dataclass).
        if not isinstance(raw_config, Mapping):
            raise TypeError(f"Invalid YAML config file.")

        return YamlConfig.__registry.construct_registered_dataclass(raw_config)

    @classmethod
    def _load_raw_yaml(
            cls: Type[T],
            file_path_or_stream: str | Path | IOBase | StringIO,
            safe: bool = True
    ) -> Any:
        # Deserialize the yaml into an object. If the yaml contains known
        # tags it will return the appropriate python classes, otherwise
        # it will return primitive python types (e.g., ints, floats, lists,
        # dicts, etc.)

        yaml_loader = yaml.safe_load if safe else yaml.load

        if isinstance(file_path_or_stream, (str, Path)):
            with open(file_path_or_stream, "rt") as fh:
                # This allows using paths relative to the input config file
                # rather than paths relative to the current working directory.
                with _enable_yaml_include(file_path_or_stream):
                    return yaml_loader(fh)
        else:
            with file_path_or_stream as fh:
                return yaml_loader(fh)


@config_dataclass
class EnvironmentConfig(abc.ABC):
    """A mixin clas for configuration objects to help constructing them from environment variables.

    This mixin adds a method :meth:`from_environment` that will try to parse
    environment variables into the correct type for the dataclass. All you
    have to do is implement the :meth:`environment_mapping` method to provide
    a mapping between environment variable names and the dataclass field names.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _default_type_parsers = {
        bool: lambda x: x.lower() in ("true", "1", "t", "y", "yes"),
        int: int,
        float: float,
        str: lambda x: x,
        datetime.datetime: parse_date,
        datetime.date: lambda x: parse_date(x).date(),
    }
    _dataclass_fields = None

    @classmethod
    def get_default_type_parsers(cls: Type[E]) -> dict[Type[I], TypeParser]:
        """Get the default type parsers for this class."""

        return cls._default_type_parsers.copy()

    @classmethod
    @abc.abstractmethod
    @ensure(
        lambda cls, result: all(cls._is_valid_field(v) for v in result.values()),
        "All values in the mapping must be a valid field name."
    )
    def environment_mapping(cls: Type[E]) -> Mapping[str, str]:
        """
        Returns a mapping from environment variable names to their
        corresponding field name.

        Returns
        -------
        Mapping[str, str]

        Raises
        ------
        ViolationError
            If any of the returned values are not a field name of this
            class.
        """
        pass

    @classmethod
    def from_environment(
            cls: Type[E],
            type_parsers: Optional[dict[Type[I], TypeParser]] = None,
            **kwargs
    ) -> EnvironmentConfig:
        """
        Create an instance from environment variables.

        Environment variables can represent python primitive values,
        date objects, datetime objects. They can also be lists, sets, tuples,
        or dicts of these types. Collections are space separated string.
        Multiword strings should be enclosed in double quotes. Dictionary
        key value pairs are delimited by '='. Spaces are not allowed in
        keys or values.

        Parameters
        ----------
        type_parsers: dict[Type[I], TypeParser]
            A mapping from python types to functions that parse a string
            into that type. These will be combined and override the default
            parsing rules described above.

        kwargs
            Additional keyword arguments to override the values from the
            environment or composite fields (e.g., other dataclasses),
            which are constructed externally.

        Returns
        -------

        """
        type_parsers = cls._default_type_parsers | (type_parsers or {})
        field_lookup = cls.get_dataclass_field_map()
        resolved_types = get_type_hints(cls)

        # The keyword arguments we'll use to construct the instance.
        kwargs: dict[str, Any] = kwargs.copy()

        # A utility method to make sure we get the actual field type in case
        # it is marked optional.
        def _get_actual_type(t: Type[I]) -> Type[I]:
            if get_origin(t) is Union:
                args = get_args(t)
                if len(args) == 2 and type(None) in args:
                    args = [a for a in args if a is not type(None)]
                    return args[0]
                else:
                    raise NotImplementedError(f"Unions of more than one type are not supported")
            return t

        for variable_name, field_name in cls.environment_mapping().items():
            environment_value = os.environ.get(variable_name)

            # If the environment variable doesn't exist, try to use the default
            # constructor value (or raise an exception).
            # If the kwargs already has a value for the field (as provided as
            # a parameter by the user), do not overwrite it.
            if environment_value is None or field_name in kwargs:
                continue

            field = field_lookup[field_name]
            field_type = _get_actual_type(resolved_types[field.name])
            field_value = cls.parse_environment_value(environment_value, field_type, type_parsers)

            kwargs[field_name] = field_value

        return cls(**kwargs)

    @classmethod
    def _is_valid_field(cls, field_name: str) -> bool:
        # A valid field is any field that can be used in the constructor.
        field_names = {f.name for f in dataclasses.fields(cls) if f.init}  # noqa

        return field_name in field_names

    @classmethod
    def get_dataclass_field_map(cls) -> dict[str, dataclasses.Field]:
        """Get a mapping from field names to their dataclass fields."""

        if cls._dataclass_fields is None:
            cls._dataclass_fields = {f.name: f for f in dataclasses.fields(cls)}  # noqa

        return cls._dataclass_fields

    @classmethod
    def parse_environment_value(
            cls,
            s: str,
            target_type: Type[I],
            type_parsers: dict[Type[I], TypeParser]
    ) -> I:
        """
        Try to parse an environment value expressed as a string into the given
        python ``target_type``.

        Parameters
        ----------
        s : str
            The environment value to parse.
        target_type : Type
            The python type to parse the value into.
        type_parsers : dict[Type, TypeParser], optional
            An optional dictionary that maps a type to a function that
            parses a string to that type.

        Returns
        -------
        An instance of the target type parsed from the environment value.
        """
        # Convenience method so we don't have to types so much.
        parse_value = lambda x, t: cls.parse_environment_value(x, t, type_parsers)
        origin = get_origin(target_type)

        if origin is None:
            try:
                return type_parsers[target_type](s)
            except (ValueError, TypeError):
                raise ValueError(f"Unable to parse '{s}' as {target_type}.")
            except KeyError:
                raise TypeError(f"Unsupported primitive type: {target_type}")
            except Exception as e:
                raise e

        if origin in (list, tuple, set):
            item_type = get_args(target_type)[0]
            as_list = [parse_value(v, item_type) for v in cls._split_with_quotes(s)]

            if origin is tuple:
                return tuple(as_list)
            elif origin is set:
                return set(as_list)

            return as_list

        if origin is dict:
            key_type, value_type = get_args(target_type)
            as_list = cls._split_with_quotes(s)
            as_pairs = [i.split("=") for i in as_list]
            as_tuples = [
                (parse_value(k, key_type), parse_value(v, value_type))
                for k, v in as_pairs
            ]
            return dict(as_tuples)

        raise TypeError(f"Unsupported type: {target_type}")

    @classmethod
    def _split_with_quotes(cls, s: str) -> list[str]:
        matches = re.findall(r"\"(.+?)\"|(\S+)", s)

        return [m[0] if m[0] else m[1] for m in matches]
