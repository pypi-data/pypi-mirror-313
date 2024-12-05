import sys
from importlib import import_module
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import find_spec
from types import ModuleType
from typing import Any, Optional


class AtlantisFinder(MetaPathFinder):
    finding_in_atlantis: bool = False

    @classmethod
    def find_spec(cls, fullname: str, *args, **kwargs) -> Optional[ModuleSpec]:
        if "atlantiscore" not in fullname:
            return None

        if cls.finding_in_atlantis:
            return None

        cls.finding_in_atlantis = True
        if find_spec(fullname):
            cls.finding_in_atlantis = False
            return None

        cls.finding_in_atlantis = False
        return ModuleSpec(fullname, cls)

    @classmethod
    def create_module(cls, spec: ModuleSpec) -> Any:
        redirected_name = spec.name.replace(
            "atlantiscore",
            "codercore",
        )
        try:
            return import_module(redirected_name)
        except ModuleNotFoundError as e:
            try:
                return cls.import_attribute(*redirected_name.rsplit(".", 1))
            except (AttributeError, ModuleNotFoundError, TypeError):
                raise e

    @staticmethod
    def import_attribute(module_name: str, attr_name: str) -> Any:
        return getattr(import_module(module_name), attr_name)

    @staticmethod
    def exec_module(module: ModuleType) -> None:
        # Intentionally left blank.
        pass


sys.meta_path.append(AtlantisFinder())
