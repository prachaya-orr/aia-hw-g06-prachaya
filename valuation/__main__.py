"""CLI: .venv/bin/python -m valuation <คำสั่ง> <TICKER>

  fetch  ดึงข้อมูลดิบลง data/raw/<TICKER>.json [--peers A B C]
  draft  ร่าง assumptions/<TICKER>.yaml จากข้อมูลดิบ (ไม่เขียนทับไฟล์เดิม)
  run    คำนวณทุกวิธีแล้วสร้าง Excel + results.json ใน output/<TICKER>/ [--refetch]
  verify ให้ LibreOffice คำนวณ Excel ใหม่แล้วเทียบกับ Python
"""
from __future__ import annotations

import argparse
import sys

from . import fetch


def main() -> int:
    ap = argparse.ArgumentParser(prog="python -m valuation")
    sub = ap.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fetch", help="ดึงข้อมูลดิบลง data/raw/<TICKER>.json")
    f.add_argument("ticker", help="เช่น CPALL.BK หรือ AAPL")
    f.add_argument("--peers", nargs="*", default=[], help="ticker ของ peer สำหรับ comps (ผู้เรียนยืนยันแล้ว)")
    f.add_argument("--minority-proxy", help="บริษัทลูกที่จดทะเบียน ใช้ P/BV ปรับ minority interest เป็นมูลค่าตลาด")

    for cmd, desc in (("draft", "ร่างสมมติฐาน"), ("run", "คำนวณและสร้างไฟล์ผลลัพธ์")):
        p = sub.add_parser(cmd, help=desc)
        p.add_argument("ticker")
        p.add_argument("--refetch", action="store_true", help="ดึงข้อมูลใหม่แม้มี data/raw อยู่แล้ว")
    v = sub.add_parser("verify", help="เทียบ Excel กับ Python")
    v.add_argument("ticker")

    args = ap.parse_args()
    ticker = args.ticker.strip().upper()
    if args.cmd == "fetch":
        return fetch.main(ticker, args.peers, args.minority_proxy)
    from . import pipeline, verify
    if args.cmd == "draft":
        return pipeline.draft(ticker, args.refetch)
    if args.cmd == "run":
        return pipeline.run(ticker, args.refetch)
    return verify.main(ticker)


if __name__ == "__main__":
    sys.exit(main())
