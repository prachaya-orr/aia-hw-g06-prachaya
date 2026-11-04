"""สร้าง output/<TICKER>/<TICKER>_valuation.html จาก results.json ด้วย jinja2

ไฟล์เดียว เปิดได้แบบ offline (ไม่โหลดอะไรจากเน็ต) รองรับ dark mode และจอโทรศัพท์
football field เป็นแท่ง HTML/CSS วางตำแหน่งเป็น % จึงย่อตามจอได้โดยตัวหนังสือไม่เล็กลง
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import CFG
from .methods import LABELS, MULTIPLE_NAMES

V = CFG["valuation"]
S = V["sensitivity"]
TEMPLATES = Path(__file__).resolve().parent / "templates"

SYMBOL = {"THB": "฿", "USD": "$", "JPY": "¥", "EUR": "€"}
KIND = {"fact": "ข้อเท็จจริง", "derived": "คำนวณจากอดีต", "assumption": "สมมติฐาน"}


def nice_step(span: float, n: int = 5) -> float:
    raw = span / n
    mag = 10 ** math.floor(math.log10(raw))
    return next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)


def football(res: dict) -> dict:
    rows = [r for r in res["results"] if not r["skipped"]]
    vals = [v for r in rows for v in (r["low"], r["high"]) if v is not None] + [res["price"]]
    lo, hi = min(vals), max(vals)
    if lo > 0:
        lo = max(0.0, lo - (hi - lo) * 0.15)
    step = nice_step(hi - lo)
    lo, hi = math.floor(lo / step) * step, math.ceil(hi / step) * step

    def pos(v: float) -> float:
        return round((v - lo) / (hi - lo) * 100, 3)

    bars = []
    for r in rows:
        bars.append({**r, "left": pos(r["low"]), "width": max(pos(r["high"]) - pos(r["low"]), 0.6),
                     "base_pos": pos(r["base"]) if r["base"] is not None else None,
                     "reading": reading(res["price"], r["low"], r["high"])})
    ticks = [{"value": lo + i * step, "pos": pos(lo + i * step)} for i in range(round((hi - lo) / step) + 1)]
    return {"bars": bars, "ticks": ticks, "price_pos": pos(res["price"]), "zero_pos": pos(0) if lo < 0 else None}


def reading(price: float, low: float, high: float) -> str:
    if price < low:
        return "ราคาต่ำกว่าช่วง"
    if price > high:
        return "ราคาสูงกว่าช่วง"
    return "ราคาอยู่ในช่วง"


def sources(res: dict) -> list[dict]:
    seen = {}
    for k, inp in res["inputs"].items():
        if inp["kind"] == "assumption" and not inp["url"]:
            continue
        key = (inp["source"], inp["url"])
        seen.setdefault(key, {"source": inp["source"], "url": inp["url"], "asof": inp["asof"], "used": []})
        seen[key]["used"].append(inp["label"])
    for sym, d in res["peers"].items():
        for fld in ("trailing_pe", "ev_to_ebitda"):
            f = d[fld]
            key = (f["source"], f["url"])
            seen.setdefault(key, {"source": f["source"], "url": f["url"], "asof": f["asof"], "used": []})
            seen[key]["used"].append(f"{MULTIPLE_NAMES[fld]} ของ {sym}")
    return list(seen.values())


def build(res: dict, path: Path) -> Path:
    cur = res["company"]["currency"]
    sym = SYMBOL.get(cur, "")
    fin = res["company"]["financial_currency"]

    def ps(v):
        if v is None:
            return "–"
        sign = "−" if v < 0 else ""
        return f"{sign}{sym}{abs(v):,.2f}" if sym else f"{sign}{abs(v):,.2f} {cur}"

    def money(v):
        if v is None:
            return "–"
        return f"{'−' if v < 0 else ''}{abs(v) / 1e9:,.1f} พันล้าน {fin}"

    def pct(v, d=2):
        return "–" if v is None else f"{v * 100:.{d}f}%"

    def mult(v):
        return "–" if v is None else f"{v:.2f}×"

    def fmt(v, unit):
        if isinstance(v, bool):
            return "ใช่" if v else "ไม่ใช่"
        if isinstance(v, str):
            return v
        if isinstance(v, list):
            return " · ".join(fmt(x, unit) for x in v)
        return {"%": pct, "money": money, "สกุลงบ": money, "per_share": ps, "ต่อหุ้น": ps, "x": mult,
                "เท่า": lambda x: f"{x:.3f}", "beta": lambda x: f"{x:.2f}", "หุ้น": lambda x: f"{x:,.0f}"}.get(unit, str)(v)

    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.filters.update(ps=ps, money=money, pct=pct, mult=mult)
    env.globals.update(fmt=fmt, KIND=KIND, LABELS=LABELS)
    results = {r["key"]: r for r in res["results"]}
    ok = [x for x in res["results"] if not x["skipped"]]
    dcf = results.get("dcf_fcff")
    # ขั้นของ DCF แบ่งเป็นส่วน discount rate (ถึงขั้น WACC) กับส่วนจาก FCFF เป็นราคาต่อหุ้น
    split = next((i + 1 for i, s in enumerate(dcf["steps"]) if s["label"] == "WACC"), 0) if dcf else 0
    html = env.get_template("report.html").render(
        r=res, ff=football(res), results=results, sources=sources(res), S=S, V=V, dcf=dcf, split=split, ok=ok,
        skipped=[x for x in res["results"] if x["skipped"]],
        not_used=len(set(res["method_reasons"]) - {x["key"] for x in ok}),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


# ---------- หน้าแรกของ GitHub Pages ----------

READING_CLASS = {"ราคาต่ำกว่าช่วง": "below", "ราคาสูงกว่าช่วง": "above", "ราคาอยู่ในช่วง": ""}


def build_index(root: Path) -> Path:
    """index.html ที่ root ของ repo: การ์ดของหุ้นทุกตัวใน output/ ลิงก์ไปหน้า HTML, Excel และเหตุผลการเลือกวิธี

    ไฟล์ .md ลิงก์ไปหน้า GitHub เพราะ .nojekyll ทำให้ GitHub Pages ไม่แปลง markdown เป็นหน้าเว็บ
    """
    site = CFG["site"]
    blob = site["repo_url"].rstrip("/") + "/blob/" + site["branch"] + "/"
    stocks = []
    for res_path in sorted((root / V["output_dir"]).glob("*/*_results.json")):
        res = json.loads(res_path.read_text(encoding="utf-8"))
        sym = SYMBOL.get(res["company"]["currency"], "")
        t = res["ticker"]
        rel = f"{V['output_dir']}/{t}/{t}_valuation"
        methods = []
        for r in res["results"]:
            if r["skipped"]:
                continue
            rd = reading(res["price"], r["low"], r["high"])
            methods.append({"label": r["label"], "low": f"{sym}{r['low']:,.2f}", "high": f"{sym}{r['high']:,.2f}",
                            "base": "–" if r["base"] is None else f"{sym}{r['base']:,.2f}",
                            "reading": rd, "cls": READING_CLASS[rd]})
        stocks.append({"ticker": t, "name": res["company"]["long_name"], "status": res["status"],
                       "industry": f"{res['company']['sector']} · {res['company']['industry']}",
                       "price": f"{sym}{res['price']:,.2f}", "fetched": res["fetched_at"][:10], "methods": methods,
                       "html": f"{rel}.html", "xlsx": f"{rel}.xlsx", "choice": f"{blob}{res['method_choice']}"})
    docs = [{"label": d["label"], "note": d["note"], "url": blob + d["path"]} for d in site["docs"]]
    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    path = root / "index.html"
    path.write_text(env.get_template("index.html").render(stocks=stocks, docs=docs), encoding="utf-8")
    return path
