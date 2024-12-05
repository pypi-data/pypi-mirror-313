import io
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, ValidationError

from .print_ import PrintFormat, print_console, print_json, print_plain, print_table
from .str import str_to_list
from .zip import read_text_from_zip_archive


class BaseConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @classmethod
    def to_list_str_validator(
        cls,
        v: str | list[str] | None,
        *,
        lower: bool = False,
        unique: bool = False,
        remove_comments: bool = False,
        split_line: bool = False,
    ) -> list[str]:
        if v is None:
            return []
        if isinstance(v, str):
            return str_to_list(v, unique=unique, remove_comments=remove_comments, split_line=split_line, lower=lower)
        return v

    @classmethod
    def read_config[T](  # nosec: B107
        cls: type[T],
        config_path: io.TextIOWrapper | str | Path,
        error_print_type: PrintFormat = PrintFormat.PLAIN,
        zip_password: str = "",
    ) -> T:
        try:
            # is it zip archive?
            if isinstance(config_path, str) and config_path.endswith(".zip"):
                config_path = str(Path(config_path).expanduser())
                return cls(**yaml.full_load(read_text_from_zip_archive(config_path, password=zip_password)))
            if isinstance(config_path, io.TextIOWrapper) and config_path.name.endswith(".zip"):
                config_path = str(Path(config_path.name).expanduser())
                return cls(**yaml.full_load(read_text_from_zip_archive(config_path, password=zip_password)))
            if isinstance(config_path, Path) and config_path.name.endswith(".zip"):
                config_path = str(config_path.expanduser())
                return cls(**yaml.full_load(read_text_from_zip_archive(config_path, password=zip_password)))

            # plain yml file
            if isinstance(config_path, str):
                return cls(**yaml.full_load(Path(config_path).expanduser().read_text()))
            elif isinstance(config_path, Path):
                return cls(**yaml.full_load(config_path.expanduser().read_text()))
            else:
                return cls(**yaml.full_load(config_path))
        except ValidationError as err:
            print_plain("config validation errors", error_print_type)
            json_errors = []
            rows = []
            for e in err.errors():
                loc = e["loc"]
                field = ".".join(str(lo) for lo in loc) if len(loc) > 0 else ""
                print_plain(f"{field} {e['msg']}", error_print_type)
                json_errors.append({field: e["msg"]})
                rows.append([field, e["msg"]])
            print_table("config validation errors", ["field", "message"], rows)
            print_json({"errors": json_errors}, error_print_type)
            exit(1)
        except Exception as err:
            if error_print_type == "json":
                print_json({"exception": str(err)})
            else:
                print_console(f"config error: {err!s}")
            exit(1)
