#!/usr/bin/env python3
"""Copier entrypoint: copies entry.png to the grader output directory.

Deterministic: byte-for-byte copy, no timestamps, no randomness.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print("copied", SRC, "->", DST)


if __name__ == "__main__":
    main()
