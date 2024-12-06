import os
import zipfile
from typing import Literal


def compress_dir_path(dir_path: str, compress_type: Literal["zip"] = "zip"):
    dir_path = os.path.abspath(dir_path)
    if not os.path.isdir(dir_path):
        raise ValueError(f"不支持 dir_path：{dir_path}！")

    valid_compress_type = ["zip"]
    if compress_type not in valid_compress_type:
        raise ValueError(f"不支持 compress_type：{compress_type}！")

    compress_file_path = os.path.join(
        os.path.dirname(dir_path), os.path.basename(dir_path) + "." + compress_type
    )

    if compress_type == "zip":
        with zipfile.ZipFile(compress_file_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_file_path = os.path.relpath(file_path, dir_path)
                    zf.write(file_path, arcname=rel_file_path)
