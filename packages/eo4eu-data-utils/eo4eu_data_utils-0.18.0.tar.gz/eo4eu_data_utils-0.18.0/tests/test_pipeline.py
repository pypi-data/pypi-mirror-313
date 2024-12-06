from eo4eu_data_utils.config import Config, Try, default_boto_config
from eo4eu_data_utils.pipeline import Pipeline, S3Driver, then
from pprint import pprint
from pathlib import Path
try:
    from typing import Self
except Exception:
    from typing_extensions import Self
from enum import Enum
import logging
import re

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

unfilled_config = Config(
    boto = default_boto_config,
    bucket = "apollo-test"
)


class FileKind(Enum):
    ARCH = 0
    DATA = 1
    META = 2
    TIFF = 3
    OTHER = 4

    @classmethod
    def from_path(cls, path: Path) -> Self:
        extension = path.suffix
        # handle cases such as .tar.gz
        if len(path.suffixes) > 1 and path.suffixes[-2] == ".tar":
            extension = "".join(path.suffixes[-2:])

        if extension in {".tar", ".tar.gz", ".tar.br", ".tar.xz"}:
            return cls.ARCH

        if extension in {
            ".json", ".csv", ".xml", ".xls", ".xlsx", ".xlsb",
            ".xlsm", ".odf", ".ods", ".odt", ".dbf"
        }:
            if re.match(f"(.*\-)?meta.*\.json", path.name):
                return cls.META
            return cls.DATA

        if extension in {".tiff", "tif"}:
            return cls.TIFF

        return cls.OTHER


if __name__ == "__main__":
    config = unfilled_config.use_env().fill()
    s3_driver = S3Driver(
        config = config.boto.to_dict(),
        bucket = config.bucket
    )

    pipeline = Pipeline(
        logger = logger,
        summary = logger,
        selector = FileKind.from_path
    )

    result = (pipeline
        .source(s3_driver)
        .switch(
            cases = {
                FileKind.DATA: then().summarize("Downloading files...")
                                     .download("final"),
                FileKind.ARCH: then().download("temp")
                                     .unpack("unpack")
                                     .filter(FileKind.DATA)
                                     .move("final"),
                FileKind.TIFF: then().consume("tiffs")
            },
            otherwise = then().consume("other")
        )
        .consume("downloaded")
        .exec()
    )

    pprint(result)
