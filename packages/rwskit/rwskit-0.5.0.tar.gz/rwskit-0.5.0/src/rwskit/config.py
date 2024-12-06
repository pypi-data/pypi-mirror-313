from __future__ import annotations


# Python Modules
import dataclasses
import datetime
import logging

from contextlib import contextmanager
from io import IOBase, StringIO

from pathlib import Path
from typing import Any, ClassVar, Iterable, Mapping, Type, TypeVar

# 3rd Party Modules
import yaml
import yaml_include
from icontract import require

from dateutil.parser import parse as parse_date
from pydantic.dataclasses import dataclass as pydantic_dataclass
from yamlable import YamlAble

# Project Modules
from rwskit.dataclasses_ import DataclassRegistry
from rwskit.types_ import get_qualified_name

log = logging.getLogger(__name__)


T = TypeVar("T", bound="YamlConfig")


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
