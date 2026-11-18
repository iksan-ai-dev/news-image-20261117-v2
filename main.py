#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to the output directory.

Stdlib only. The image is rendered at build time by compose.py and shipped
as entry.png next to this file, so the program is deterministic: every run
writes identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
