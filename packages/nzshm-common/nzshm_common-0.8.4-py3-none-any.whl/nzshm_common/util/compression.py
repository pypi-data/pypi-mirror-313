import base64
import io
import zipfile
from pathlib import Path, PurePath
from typing import Union


def compress_path(source_path: str, output_zip: Union[str, PurePath], compression=zipfile.ZIP_DEFLATED) -> str:
    """Zip contents of source path and return the archive path.

    Handles both single file and a folder.
    """
    with zipfile.ZipFile(output_zip, "w", compression=compression) as zf:
        if Path(source_path).is_file():
            zf.write(source_path, PurePath(source_path).name)
        else:
            for filename in Path(source_path).rglob("*"):
                zf.write(filename, arcname=str(Path(filename).relative_to(source_path)))
    return str(output_zip)


def compress_string(data: str, compression=zipfile.ZIP_LZMA) -> str:
    """Use compression to pack this string into a much smaller string."""
    compressed = io.BytesIO()
    with zipfile.ZipFile(compressed, "w", compression=compression) as zf:
        zf.writestr("0", data)
    compressed.seek(0)
    b64 = base64.b64encode(compressed.read())
    return b64.decode("ascii")


def decompress_string(compressed: str) -> str:
    """Decompress a ZIP compressed string to the original string."""
    base64_bytes = compressed.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    with zipfile.ZipFile(io.BytesIO(message_bytes)) as zf:
        b64 = io.BytesIO(zf.read("0"))
    b64.seek(0)
    return b64.read().decode("utf-8")
