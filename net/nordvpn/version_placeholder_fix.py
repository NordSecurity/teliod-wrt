#!/usr/bin/env python3
import sys
import re

if len(sys.argv) != 3:
    sys.exit(f"Usage: {sys.argv[0]} <file> <version>")

teliod_path, version = sys.argv[1], sys.argv[2]

with open(teliod_path, "rb") as f:
    data = f.read()

m = re.search(br"VERSION_PLACEHOLDER@+\x00", data)
if not m:
    sys.exit("ERROR: version placeholder not found")

start, end = m.span()
field_len = end - start
max_len = field_len - 1  # subtract the final NUL

print(f"Replacing version placeholder in {teliod_path} with '{version}'")
print(f"Field length: {field_len} bytes, max_length: {max_len} bytes")

if len(version) > max_len:
    sys.exit(f"ERROR: version too long (max {max_len} bytes)")

# Construct replacement string that's padded with NULs
repl = version.encode() + b"\x00"
repl = repl.ljust(field_len, b"\x00")

newdata = data[:start] + repl + data[end:]

with open(teliod_path, "wb") as f:
    f.write(newdata)
