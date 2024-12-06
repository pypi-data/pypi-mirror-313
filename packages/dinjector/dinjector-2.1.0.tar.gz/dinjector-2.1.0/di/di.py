"""Implement dependency injections between beans of application.

Simplify the construction of applications.
"""
import abc
import importlib
from dataclasses import dataclass
from typing import Any

import yaml


class ConfigService(abc.ABC):
    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        ...


@dataclass(frozen=True)
class BeanDefinition:
    module_name: str
    class_name: str
    args: str | list = ""
    kwargs: str | dict[str, Any] = ""

    def import_class(self, module_base: str = ""):
        module_name = (
            f"{module_base}.{self.module_name}" if module_base else self.module_name
        )
        module = importlib.import_module(module_name)
        return getattr(module, self.class_name)

    @classmethod
    def from_dict(cls, value):
        return cls(
            value["module"],
            value["class"],
            value.get("args", []),
            value.get("kwargs", {}),
        )


class DependencyInjector:
    """Assure the correct injection of bean components to construct all application."""

    def __init__(
        self,
        config_service: ConfigService,
        dependencies_fn: str,
        module_base: str = "",
    ):
        self._config = config_service
        self._base = module_base
        self._beans = {}
        with open(dependencies_fn, "r") as f:
            self._dependencies = yaml.load(f, Loader=yaml.FullLoader)

    def construct(self, bean_name):
        """Create object by its bean name."""
        bean_dict = self._dependencies[bean_name]
        definition = BeanDefinition.from_dict(bean_dict)
        Class = definition.import_class(self._base)
        args = []
        def_args = definition.args
        if def_args:
            if type(def_args) is str and def_args[0] == "$":
                def_args = self._config[def_args[1:]]

            for arg in def_args:
                if type(arg) is not str:
                    args.append(arg)
                elif arg[0] == ">":
                    args.append(self[arg[1:]])
                elif arg[0] == "$":
                    args.append(self._config[arg[1:]])
                elif arg[0] == "+":
                    args.append(self.construct(arg[1:]))
                else:
                    args.append(arg)

        kwargs = {}
        def_kwargs = definition.kwargs
        if def_kwargs:
            if type(def_kwargs) is str and def_kwargs[0] == "$":
                kwargs = self._config[def_kwargs[1:]]
            elif type(def_kwargs) is dict:
                for key, value in def_kwargs.items():
                    if type(value) is not str:
                        value_ = value
                    elif value[0] == ">":
                        value_ = self[value[1:]]
                    elif value[0] == "$":
                        value_ = self._config[value[1:]]
                    elif value[0] == "+":
                        value_ = self.construct(value[1:])
                    else:
                        value_ = value
                    kwargs[key] = value_
            else:
                raise ValueError(f"{def_kwargs} can not be processed")

        return Class(*args, **kwargs)

    def __getitem__(self, bean_name: str):
        """Return a singleton bean"""
        if bean_name not in self._beans:
            self._beans[bean_name] = self.construct(bean_name)

        return self._beans[bean_name]
