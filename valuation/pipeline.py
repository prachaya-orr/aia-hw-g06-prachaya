"""ลำดับงานของ 1 ticker: (fetch) -> สมมติฐาน -> methods -> Excel + results.json"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import yaml

from . import CFG, ROOT
from . import assumptions as A
from . import excel, fetch, html, methods

V = CFG["valuation"]


def raw_path(ticker: str) -> Path:
    return fetch.RAW_DIR / f"{ticker}.json"


def out_dir(ticker: str) -> Path:
    return ROOT / V["output_dir"] / ticker


def load_raw(ticker: str) -> dict:
    return json.loads(raw_path(ticker).read_text(encoding="utf-8"))


def requested(ticker: str) -> tuple[list[str], str | None]:
    """peer และ minority proxy ที่ระบุในไฟล์สมมติฐาน ถ้ายังไม่มีไฟล์ ใช้ค่าจากข้อมูลดิบเดิม"""
    path = A.path_for(ticker)
    if path.exists():
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        return doc.get("peers") or [], doc.get("minority_proxy")
    if raw_path(ticker).exists():
        raw = load_raw(ticker)
        return raw["peers"]["requested"], (raw.get("minority_proxy") or {}).get("requested")
    return [], None


def ensure_raw(ticker: str, refetch: bool) -> dict:
    peers, proxy = requested(ticker)
    have = False
    if raw_path(ticker).exists():
        raw = load_raw(ticker)
        have = (raw.get("schema_version") == fetch.SCHEMA_VERSION
                and set(raw["peers"]["requested"]) == set(peers)
                and (raw.get("minority_proxy") or {}).get("requested") == proxy)
    if refetch or not have:
        code = fetch.main(ticker, peers, proxy)
        if code:
            raise SystemExit(f"fetch {ticker} ไม่ผ่าน (exit {code})")
    return load_raw(ticker)


def draft(ticker: str, refetch: bool) -> int:
    raw = ensure_raw(ticker, refetch)
    path = A.write_draft(raw)
    print(f"ร่างสมมติฐาน {path.relative_to(ROOT)} แล้ว รีวิวและอ้าง playbook ก่อนเปลี่ยน status เป็น reviewed")
    return 0


def to_jsonable(a: A.Assumptions, raw: dict, out: dict) -> dict:
    return {
        "ticker": a.ticker,
        "status": a.status,
        "method_choice": a.method_choice,
        "method_reasons": a.method_reasons,
        "limitations": a.limitations,
        "price": a["price"],
        "fetched_at": raw["fetched_at"],
        "company": {k: raw["info"][k]["value"] for k in ("long_name", "sector", "industry", "country", "currency",
                                                          "financial_currency")},
        "inputs": {k: asdict(i) | {"label": i.label, "unit": i.unit} for k, i in a.inputs.items()},
        "peers": {s: raw["peers"]["data"][s] for s in a.peers if s in raw["peers"]["data"]},
        "wacc": out["wacc"],
        "results": [asdict(r) | {"label": r.label} for r in out["results"]],
        "warnings": out["warnings"],
    }


def run(ticker: str, refetch: bool) -> int:
    raw = ensure_raw(ticker, refetch)
    if not A.path_for(ticker).exists():
        A.write_draft(raw)
        print(f"ยังไม่มีสมมติฐาน ร่างไว้ที่ {A.path_for(ticker).relative_to(ROOT)} รีวิวก่อนแล้วรันใหม่")
        return 3
    a = A.load(ticker, raw)
    out = methods.run(a, raw["peers"]["data"])
    d = out_dir(ticker)
    xlsx = excel.build(a, raw, out, d / f"{ticker}_valuation.xlsx")
    res = d / f"{ticker}_results.json"
    payload = to_jsonable(a, raw, out)
    res.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    page = html.build(payload, d / f"{ticker}_valuation.html")
    print(f"สถานะสมมติฐาน: {a.status} · WACC {out['wacc']['wacc']:.2%} · ราคา {a['price']}")
    for r in out["results"]:
        if r.skipped:
            print(f"  {r.label}: ข้าม ({r.skipped})")
        else:
            base = f"{r.base:,.2f}" if r.base is not None else "-"
            print(f"  {r.label}: {r.low:,.2f} – {r.high:,.2f} (base {base})")
    for w in out["warnings"]:
        print(f"  คำเตือน: {w}")
    print(f"บันทึก {xlsx.relative_to(ROOT)} · {page.relative_to(ROOT)} · {res.relative_to(ROOT)}")
    return 0
