#!/usr/bin/env python
"""
Download the latest lucide zip file and select only the optimized icons.
Also extracts alias mappings from icon metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from io import BytesIO
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="dotted version number")
    args = parser.parse_args(argv)
    version: str = args.version

    proc = subprocess.run(
        [
            "curl",
            "--fail",
            "--location",
            f"https://github.com/lucide-icons/lucide/releases/download/{version}/lucide-icons-{version}.zip",
        ],
        stdout=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise SystemExit(1)

    input_zip = ZipFile(BytesIO(proc.stdout))
    input_prefix = "icons/"

    output_path = "src/lucide/lucide.zip"
    aliases_path = "src/lucide/aliases.json"

    # Extract aliases from JSON metadata
    aliases: dict[str, str] = {}
    for name in input_zip.namelist():
        if name.startswith(input_prefix) and name.endswith(".json"):
            try:
                content = json.loads(input_zip.read(name))
                icon_name = name[len(input_prefix) :].replace(".json", "")
                if "aliases" in content and content["aliases"]:
                    for alias in content["aliases"]:
                        if isinstance(alias, dict) and "name" in alias:
                            aliases[alias["name"]] = icon_name
                        elif isinstance(alias, str):
                            aliases[alias] = icon_name
            except (json.JSONDecodeError, KeyError):
                pass

    # Write aliases file
    with open(aliases_path, "w") as f:
        json.dump(aliases, f, indent=2, sort_keys=True)
    print(f"✅ Written {len(aliases)} aliases to {aliases_path}")

    # Write icons zip
    try:
        os.remove(output_path)
    except FileNotFoundError:
        pass

    icon_count = 0
    with ZipFile(
        output_path, "w", compression=ZIP_DEFLATED, compresslevel=9
    ) as output_zip:
        for name in sorted(input_zip.namelist()):
            if name.startswith(input_prefix) and name.endswith(".svg"):
                info = input_zip.getinfo(name)
                data = input_zip.read(name).replace(b' data-slot="icon"', b"")

                new_name = name[len(input_prefix) :]

                info.filename = new_name
                output_zip.writestr(info, data)
                print(new_name)
                icon_count += 1

    print(f"\n✅ Written {icon_count} icons to {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
