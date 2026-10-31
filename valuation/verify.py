"""ตรวจว่า Excel คำนวณได้ตรงกับ Python และทุก input มีที่มา

ให้ LibreOffice (soffice) คำนวณสูตรใหม่ในโฟลเดอร์ชั่วคราว แล้วอ่านค่าที่คำนวณได้เทียบกับ results.json
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from openpyxl import load_workbook

from .pipeline import out_dir

TOLERANCE = 0.005   # ต่างกันได้ไม่เกิน 0.5% (spec ข้อ 5)

NAMES = {
    "dcf_fcff": ("x_dcf_low", "x_dcf_base", "x_dcf_high"),
    "ddm": ("x_ddm_low", "x_ddm_base", "x_ddm_high"),
    "comps_pe": ("x_comps_pe_low", "x_comps_pe_base", "x_comps_pe_high"),
    "comps_ev_ebitda": ("x_comps_ev_ebitda_low", "x_comps_ev_ebitda_base", "x_comps_ev_ebitda_high"),
    "comps_pb": ("x_comps_pb_low", "x_comps_pb_base", "x_comps_pb_high"),
    "week52": ("in_week52_low", None, "in_week52_high"),
}


def recalc(xlsx: Path, workdir: Path) -> Path:
    soffice = shutil.which("soffice")
    if not soffice:
        raise SystemExit("ไม่พบ soffice (LibreOffice) จึงคำนวณสูตรใหม่ไม่ได้")
    subprocess.run([soffice, "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(workdir), str(xlsx)],
                   check=True, capture_output=True, timeout=180)
    return workdir / xlsx.name


def named_value(wb, nm: str):
    dn = wb.defined_names[nm]
    sheet, cell = next(dn.destinations)
    return wb[sheet][cell.replace("$", "")].value


def main(ticker: str) -> int:
    d = out_dir(ticker)
    res = json.loads((d / f"{ticker}_results.json").read_text(encoding="utf-8"))
    problems = []
    for k, inp in res["inputs"].items():
        if not inp["source"]:
            problems.append(f"input {k} ไม่มี source")
        if inp["kind"] == "fact" and not inp["url"]:
            problems.append(f"input {k} เป็น fact แต่ไม่มี url")

    with tempfile.TemporaryDirectory() as tmp:
        wb = load_workbook(recalc(d / f"{ticker}_valuation.xlsx", Path(tmp)), data_only=True)
        checks = [("Rf", "x_rf", res["wacc"]["rf"]), ("Ke", "x_ke", res["wacc"]["ke"]),
                  ("Kd", "x_kd_pre", res["wacc"]["kd"]), ("WACC", "x_wacc", res["wacc"]["wacc"])]
        for r in res["results"]:
            if r["skipped"]:
                continue
            for nm, py in zip(NAMES[r["key"]], (r["low"], r["base"], r["high"])):
                if nm and py is not None:
                    checks.append((r["label"], nm, py))
        worst = 0.0
        for label, nm, py in checks:
            xl = named_value(wb, nm)
            if not isinstance(xl, (int, float)):
                problems.append(f"{label} {nm}: Excel ได้ {xl!r}")
                continue
            diff = abs(xl - py) / abs(py) if py else abs(xl)
            worst = max(worst, diff)
            mark = "ok" if diff <= TOLERANCE else "ต่างเกิน"
            print(f"  {mark:8} {label:24} {nm:26} python {py:,.6f} · excel {xl:,.6f} · ต่าง {diff:.4%}")
            if diff > TOLERANCE:
                problems.append(f"{label} {nm} ต่างกัน {diff:.2%}")
    print(f"ตรวจ {len(checks)} ค่า ต่างมากสุด {worst:.4%}")
    for p in problems:
        print(f"  ปัญหา: {p}")
    return 1 if problems else 0
