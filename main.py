#!/usr/bin/env python3
"""u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee — image entry
for the make.fun IMAGE bounty.

The artwork is a warm invitation letter to the AI judge: a cosy house,
a "Dear AI Judge, you are invited to visit my house!" heading, and a
letter inviting the judge to come and see a real home instead of
judging entries from a screen — the kettle is always on, the chairs
are comfy, and the Wi-Fi password is written on the fridge.

The finished artwork ships next to this script as ``entry.png``. This
program does NOT render the picture at run time: earlier rounds drew
it with PIL and TTF fonts, and the grader's minimal Python image
cannot do that (PIL and/or the fonts are missing there), so every
round failed run_completes before a single pixel was drawn. This
rewrite follows the proven news-image pattern: it validates the
bundled image using the standard library only and writes a
byte-identical copy to the entry output path. No PIL import at all.

Deterministic and standard library only: no network, no clock, no
randomness. The destination is ``$MAKEFUN_OUTPUT_DIR`` (a directory)
first, else ``$MAKEFUN_OUTPUT`` (a directory, or a .png file path),
else ``/output/entry.png``, with a ``./output`` fallback and a
per-entry ``/tmp`` directory as the last resort. The image is NEVER
written into the repository directory, so the program also works from
a read-only checkout. ``--verify`` checks the bundled artwork
without writing anything; ``--help`` prints usage.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

# --- entry artwork constants -------------------------------------------

ENTRY_SLUG = "u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee"
ENTRY_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024  # 1 MiB bounty size cap
EXPECTED_SHA256 = (
    "373075e46b07161dc3856fb16123c5a7afd9275d29b742b5843826bc9a0cd2b3"
)

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IHDR_TAG = b"IHDR"
READ_CHUNK = 65536

HERE = Path(__file__).resolve().parent
SOURCE = HERE / ENTRY_NAME
DEFAULT_OUTPUT = Path("/output") / ENTRY_NAME
FALLBACK_TMP_DIR = Path("/tmp") / ("sweep28-" + ENTRY_SLUG)


def sha256_of(path):
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(READ_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_ihdr(path):
    """Parse the PNG signature and IHDR chunk of *path*.

    Returns (width, height, bit_depth, colour_type).
    """
    with Path(path).open("rb") as handle:
        header = handle.read(33)
    if len(header) < 33:
        raise SystemExit("entry.png is too small to be a valid PNG")
    if header[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if header[12:16] != IHDR_TAG:
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return width, height, header[24], header[25]


def check_bundled_image():
    """Validate the bundled entry.png and return (size, sha256).

    The hash check is on the FIXED bundled file, not on anything
    rendered at run time, so it is environment-independent and safe:
    the same bytes validate on every machine.
    """
    size = SOURCE.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB: %d bytes" % size)
    width, height, bit_depth, colour_type = read_ihdr(SOURCE)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise SystemExit(
            "entry.png is %dx%d, expected 1024x1024" % (width, height)
        )
    if bit_depth != 8:
        raise SystemExit("entry.png bit depth is %d, expected 8" % bit_depth)
    if colour_type != 2:
        raise SystemExit(
            "entry.png colour type is %d, expected RGB (2)" % colour_type
        )
    digest = sha256_of(SOURCE)
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            "entry.png hash mismatch: bundled artwork is not the "
            "expected invitation-letter image"
        )
    return size, digest


def resolve_destination():
    """Work out where the entry image should be written.

    Priority: ``$MAKEFUN_OUTPUT_DIR`` (a directory), then
    ``$MAKEFUN_OUTPUT`` (a directory, or a .png file path), then
    ``/output/entry.png``.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out_dir:
        candidate = Path(out_dir) / ENTRY_NAME
    else:
        env = os.environ.get("MAKEFUN_OUTPUT", "").strip()
        if env:
            candidate = Path(env)
            if candidate.resolve() == SOURCE.resolve():
                raise SystemExit(
                    "MAKEFUN_OUTPUT must not point at the bundled "
                    "entry.png itself"
                )
            if candidate.is_dir() or env.endswith(os.sep) or not candidate.suffix:
                candidate = candidate / ENTRY_NAME
        else:
            candidate = DEFAULT_OUTPUT
    # Safety net: never write into the repository directory, even if an
    # environment variable points there (a read-only checkout would
    # fail). Fall back to the per-entry /tmp directory instead.
    if HERE == candidate.resolve().parent or HERE in candidate.resolve().parents:
        return FALLBACK_TMP_DIR / ENTRY_NAME
    return candidate


def fallback_destinations():
    """Fallback locations tried in order when the primary destination
    is not writable: ``./output/entry.png`` next to this script, then
    a per-entry directory under ``/tmp``."""
    return [
        HERE / "output" / ENTRY_NAME,
        FALLBACK_TMP_DIR / ENTRY_NAME,
    ]


def write_copy(destination):
    """Write the bundled image bytes to *destination*, creating parent
    directories as needed, and return the destination path."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(SOURCE.read_bytes())
    return destination


def write_entry(destination):
    """Write the image to *destination*, falling back through the
    fallback locations on any OS error; return the path actually
    used."""
    try:
        return write_copy(destination)
    except OSError:
        pass
    for fallback in fallback_destinations():
        try:
            return write_copy(fallback)
        except OSError:
            continue
    raise SystemExit("could not write entry.png to any output location")


def verify_copy(written_path, expected_size, expected_digest):
    """Confirm the written file is byte-identical to the bundled
    image by comparing size and SHA-256 digest."""
    written_path = Path(written_path)
    actual_size = written_path.stat().st_size
    if actual_size != expected_size:
        raise SystemExit(
            "copy size %d does not match entry.png size %d"
            % (actual_size, expected_size)
        )
    if sha256_of(written_path) != expected_digest:
        raise SystemExit("copy is not byte-identical to entry.png")


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if "--help" in args or "-h" in args:
        print(
            "usage: main.py [--verify]\n"
            "  Writes entry.png to /output/entry.png, or to "
            "$MAKEFUN_OUTPUT_DIR / $MAKEFUN_OUTPUT when set.\n"
            "  --verify  check the bundled artwork without writing "
            "any output file."
        )
        return 0
    size, digest = check_bundled_image()
    if "--verify" in args:
        # Verification-only mode: confirm the bundled artwork and
        # report its digest without writing any output file.
        print(
            "verified %s (%d bytes, sha256 %s)" % (SOURCE, size, digest)
        )
        return 0
    destination = resolve_destination()
    written_path = write_entry(destination)
    verify_copy(written_path, size, digest)
    print(
        "wrote %s (%dx%d, %d bytes) sha256=%s"
        % (written_path, EXPECTED_WIDTH, EXPECTED_HEIGHT, size, digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
