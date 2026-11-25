"""Write the excuse entry for the Make.fun bounty
"The Excuse That Almost Works" to /output/entry.txt.

The entry is one line: the excuse a gamer texts their boss to skip
work on GTA 6 launch week. Gate: 1-140 characters, at most 20 words.
"""

import os
import tempfile

ENTRY = "Jury service summons arrived \u2014 I'm in court from 9am tomorrow and they won't let me defer it."

MAX_CHARS = 140
MAX_WORDS = 20


def validate(entry):
    if not (1 <= len(entry) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(entry)}"
        )
    words = entry.split()
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"entry must be at most {MAX_WORDS} words, got {len(words)}"
        )


def atomic_write(path, data):
    """Write data atomically: temp file in the same dir, fsync,
    chmod 0644, then rename over the target, so a crash can never
    leave a half-written entry.txt behind."""
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main():
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    atomic_write(path, ENTRY + "\n")


if __name__ == "__main__":
    main()
