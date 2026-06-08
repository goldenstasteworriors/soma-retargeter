# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path
import tempfile

import newton

import soma_retargeter.pipelines.utils as pipeline_utils


def _sonic_h2_paths():
    sonic_root = Path("/home/ykj/project/SONICMJ/GR00T-WholeBodyControl")
    mjcf_path = sonic_root / "gear_sonic/data/assets/robot_description/mjcf/h2.xml"
    mesh_dir = sonic_root / "gear_sonic/data/assets/robot_description/urdf/h2/meshes"
    return mjcf_path, mesh_dir


def _patched_h2_mjcf_path() -> Path:
    mjcf_path, mesh_dir = _sonic_h2_paths()
    if not mjcf_path.exists():
        raise FileNotFoundError(f"[ERROR]: H2 MJCF not found: {mjcf_path}")
    if not mesh_dir.exists():
        raise FileNotFoundError(f"[ERROR]: H2 mesh directory not found: {mesh_dir}")

    xml = mjcf_path.read_text(encoding="utf-8")
    xml = xml.replace('meshdir="meshes/"', f'meshdir="{mesh_dir}/"')

    out_dir = Path(tempfile.gettempdir()) / "soma_retargeter_unitree_h2"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "h2.xml"
    out_path.write_text(xml, encoding="utf-8")
    return out_path


def build_robot_builder(target_type: pipeline_utils.TargetType) -> newton.ModelBuilder:
    builder = newton.ModelBuilder()
    if target_type == pipeline_utils.TargetType.UNITREE_G1:
        builder.add_mjcf(newton.utils.download_asset("unitree_g1") / "mjcf/g1_29dof_rev_1_0.xml")
    elif target_type == pipeline_utils.TargetType.UNITREE_H2:
        builder.add_mjcf(_patched_h2_mjcf_path())
    else:
        raise ValueError(f"Unsupported robot type: {target_type}")
    return builder
