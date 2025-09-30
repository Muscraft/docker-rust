#!/usr/bin/env python3
import json
import os

DEFAULT_DEBIAN_VARIANT = "trixie"
DEFAULT_ALPINE_VERSION = "3.22"

debian_variants = {
    "bullseye": [
        "amd64", "arm/v7", "arm64", "386"
    ],
    "bookworm": [
        "amd64", "arm/v7", "arm64", "386",
        "ppc64le", "s390x"
    ],
    "trixie": [
        "amd64", "arm/v7", "arm64", "386",
        "ppc64le", "s390x", "riscv64"
    ],
}

alpine_versions = {
    "3.20": ["amd64", "arm64", "ppc64le"],
    "3.21": ["amd64", "arm64", "ppc64le"],
    "3.22": ["amd64", "arm64", "ppc64le"],
}

def arch_suffix(platform: str) -> str:
    # linux/arm/v7 -> armv7, linux/amd64 -> amd64
    part = platform.split("/", 1)[1]
    return part.replace("/", "")

def debian_entries():
    entries = []
    for variant, arches in debian_variants.items():
        for arch in arches:
            entries.append({
                "name": f"{variant}-{arch}",
                "variant": variant,
                "context": f"stable/{variant}",
                "arch": arch,
                "platform": f"linux/{arch}",
            })
            entries.append({
                "name": f"slim-{variant}-{arch}",
                "variant": f"{variant}/slim",
                "context": f"stable/{variant}/slim",
                "arch": arch,
                "platform": f"linux/{arch}",
            })
    return entries

def alpine_entries():
    entries = []
    for version, arches in alpine_versions.items():
        for arch in arches:
            entries.append({
                "name": f"alpine{version}-{arch}",
                "variant": f"alpine{version}",
                "context": f"stable/alpine{version}",
                "arch": arch,
                "platform": f"linux/{arch}",
            })
    return entries

def build_matrix():
    return {"include": debian_entries() + alpine_entries()}

def main():
    matrix = build_matrix()
   # Output the JSON string to GITHUB_OUTPUT
    print(f"matrix_data={json.dumps(matrix)}", file=open(os.environ['GITHUB_OUTPUT'], 'a'))

if __name__ == "__main__":
    main()
