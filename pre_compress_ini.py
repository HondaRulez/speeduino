import gzip
import re
import shutil
import subprocess
from pathlib import Path

src = Path("reference/speeduino-hr-dev.ini")
dst = Path("reference/speeduino-hr-dev.ini.gz")

if src.exists():
    # Process as raw bytes (exact match to Linux sed)
    raw_lines = src.read_bytes().splitlines(keepends=True)
    cleaned_lines = []
    for line in raw_lines:
        ending = b"\r\n" if line.endswith(b"\r\n") else (b"\n" if line.endswith(b"\n") else b"")
        body = line[: -len(ending)] if ending else line

        body = re.sub(b";.*", b"", body)
        body = re.sub(b"[ \t]+$", b"", body)
        if body.strip():
            cleaned_lines.append(body + ending)

    cleaned = b"".join(cleaned_lines)

    # Overwrites dst unconditionally
    try:
        import zopfli.gzip
        dst.write_bytes(zopfli.gzip.compress(cleaned))
    except ImportError:
        gzip_bin = shutil.which("gzip")
        if gzip_bin:
            res = subprocess.run([gzip_bin, "-9n"], input=cleaned, capture_output=True, check=True)
            dst.write_bytes(res.stdout)
        else:
            with open(dst, "wb") as raw_f:
                with gzip.GzipFile(filename="", mode="wb", fileobj=raw_f, compresslevel=9, mtime=0) as gz:
                    gz.write(cleaned)

    print(f"Compressed {src} -> {dst} ({dst.stat().st_size} bytes)")

