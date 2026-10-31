"""Valuation pipeline ต่อหุ้นรายตัว: fetch -> methods -> excel/html

ค่าคงที่ทั้งหมดอยู่ใน config.yaml ที่ root ของ repo
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
