from pathlib import Path

from ..tools import HLINE, INDENT, printf_block, prompt
from ..types import AnyByStrDict, StrOrPath, PathSeq

__all__ = ("load_config_data", "query_user_data",)


class InvalidConfigFileError(ValueError):
    def __init__(self, conf_path: Path, quiet: bool):
        printf_block(self, "INVALID CONFIG FILE", msg=str(conf_path), quiet=quiet)
        super().__init__(conf_path)


class MultipleConfigFilesError(ValueError):
    def __init__(self, conf_paths: PathSeq, quiet: bool):
        printf_block(self, "MULTIPLE CONFIG FILES", msg=str(conf_paths), quiet=quiet)
        super().__init__(str(conf_paths))


def load_yaml_data(
    conf_path: Path, quiet: bool = False, _warning: bool = True
) -> AnyByStrDict:
    from ruamel.yaml import YAML, YAMLError

    yaml = YAML(typ="safe")

    try:
        return dict(yaml.load(conf_path))
    except YAMLError as e:
        raise InvalidConfigFileError(conf_path, quiet) from e


def load_config_data(
    src_path: StrOrPath, quiet: bool = False, _warning: bool = True
) -> AnyByStrDict:
    """Try to load the content from a `copier.yml` or a `copier.yaml` file.
    """
    conf_paths = [
        p for p in
        Path(src_path).glob("copier.*")
        if p.is_file() and p.suffix in (".yml", ".yaml",)
    ]

    if len(conf_paths) > 1:
        raise MultipleConfigFilesError(conf_paths, quiet=quiet)
    elif len(conf_paths) == 1:
        return load_yaml_data(conf_paths[0], quiet=quiet, _warning=_warning)
    else:
        return {}


def query_user_data(default_user_data: AnyByStrDict) -> AnyByStrDict:  # pragma: no cover
    """Query to user about the data of the config file.
    """
    if not default_user_data:
        return {}
    print("")
    user_data = {}
    for key in default_user_data:
        default = default_user_data[key]
        user_data[key] = prompt(INDENT + f" {key}?", default)

    print(f"\n {INDENT} {HLINE}")
    return user_data
