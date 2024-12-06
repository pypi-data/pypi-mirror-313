from pathlib import Path
from eo4eu_base_utils import OptionalModule
from eo4eu_base_utils.typing import Any, Callable, Self

from ..result import Result
from .interface import Driver


_s3_module = OptionalModule(
    package = "eo4eu_data_utils",
    enabled_by = ["s3", "full"],
    depends_on = ["boto3", "cloudpathlib"]
)

if _s3_module.is_enabled():
    import boto3
    from cloudpathlib import CloudPath, S3Client


    class S3Driver(Driver):
        def __init__(
            self,
            config: dict[str,str],
            bucket: str,
        ):
            self.resource = boto3.resource("s3", **config)
            self.bucket = self.resource.Bucket(bucket)
            self.bucket_name = bucket
            self.bucket_path = CloudPath(
                f"s3://{bucket}",
                client = S3Client(
                    aws_access_key_id = config["aws_access_key_id"],
                    aws_secret_access_key = config["aws_secret_access_key"],
                    endpoint_url = config["endpoint_url"],
                )
            )

        def source(self, input_path: Path) -> list[Path]:
            top = self.path(input_path)
            return [
                path.relative_to(top)
                for path in top.rglob("*")
                if path.is_file()
            ]

        def upload(self, src: Path, dst: Path) -> Result:
            try:
                self.bucket.upload_file(str(src), str(dst))
                return Result.ok([dst])
            except Exception as e:
                return Result.err(f"Failed to upload file: {e}")

        def download(self, src: Path, dst: Path) -> Result:
            try:
                dst.parent.mkdir(parents = True, exist_ok = True)
                self.bucket.download_fileobj(str(src), dst.open("wb"))
                return Result.ok([dst])
            except Exception as e:
                return Result.err(f"Failed to download file: {e}")

        def get(self, path: Path) -> bytes:
            return self.resource.Object(self.bucket_name, str(path)).get()["Body"].read()

        def put(self, path: Path, data: bytes) -> Path:
            self.bucket.put_object(Key = str(path), Body = data)
            return path

        def path(self, *paths) -> CloudPath:
            return self.bucket_path.joinpath(*paths)

        def list_paths(self, *paths) -> list[str]:
            return [
                str(path.relative_to(self.bucket_path))
                for path in self.path(*paths).rglob("*")
                if path.is_file()
            ]

        def upload_file(self, src: str|Path, dst: str|Path) -> bool:
            return self.upload(Path(src), Path(dst)).is_ok()

        def download_file(self, src: str|Path, dst: str|Path) -> bool:
            return self.download(Path(src), Path(dst)).is_ok()

        def upload_bytes(self, key: str|Path, data: bytes) -> bool:
            key_str = str(key)
            try:
                self.bucket.put_object(Key = key_str, Body = data)
                return True
            except Exception as e:
                return False

        def download_bytes(self, key: str|Path) -> bytes|None:
            key_str = str(key)
            try:
                result = self.resource.Object(self.bucket_name, key_str).get()["Body"].read()
                return result
            except Exception as e:
                return None
else:
    S3Driver = _s3_module.broken_class("S3Driver")
