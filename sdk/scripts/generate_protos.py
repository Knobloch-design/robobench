"""Regenerate the gRPC Python code from robobench_sdk/proto/controller.proto.

Run after editing the .proto (requires `pip install grpcio-tools`):

    python sdk/scripts/generate_protos.py

The generated controller_pb2*.py files are committed so users installing the SDK
don't need grpcio-tools.
"""

from __future__ import annotations

import sys
from pathlib import Path

SDK_ROOT = Path(__file__).resolve().parents[1]
PROTO = Path("robobench_sdk/proto/controller.proto")


def main() -> int:
    from grpc_tools import protoc

    return protoc.main(
        [
            "grpc_tools.protoc",
            f"-I{SDK_ROOT}",
            f"-I{Path(protoc.__file__).parent / '_proto'}",
            f"--python_out={SDK_ROOT}",
            f"--pyi_out={SDK_ROOT}",
            f"--grpc_python_out={SDK_ROOT}",
            str(PROTO),
        ]
    )


if __name__ == "__main__":
    sys.exit(main())
