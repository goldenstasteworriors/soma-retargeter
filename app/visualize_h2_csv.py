#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Visualize a retargeted Unitree H2 CSV, optionally alongside its source BVH."""

from pathlib import Path
import sys

import newton.examples
import warp as wp

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app.bvh_to_csv_converter import Viewer  # noqa: E402


def main():
    parser = newton.examples.create_parser()
    parser.set_defaults(viewer="gl")
    parser.add_argument("--csv", required=True, help="Path to the retargeted H2 CSV file.")
    parser.add_argument("--bvh", default="", help="Optional source SOMA BVH file for side-by-side inspection.")
    parser.add_argument(
        "--facing",
        default="Mujoco",
        choices=["Mujoco", "Blender", "USD"],
        help="Source BVH facing-direction convention.",
    )
    viewer, args = newton.examples.init(parser)

    config = {
        "import_folder": "",
        "export_folder": "",
        "batch_size": 1,
        "retargeter": "Newton",
        "retarget_source": "soma",
        "retarget_target": "unitree_h2",
        "retarget_source_facing_direction": args.facing,
    }

    with wp.ScopedDevice(args.device):
        app = Viewer(viewer, config)
        if args.bvh:
            app.load_bvh_file(args.bvh)
        app.load_csv_file(args.csv)
        app.run()


if __name__ == "__main__":
    main()
