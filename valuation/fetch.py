"""ดึงข้อมูลดิบของหุ้น 1 ตัวลง data/raw/<TICKER>.json

แหล่ง: Yahoo Finance (yfinance) · Rf จาก ThaiBMA 10Y (ticker .BK) หรือ ^TNX (ตัวอื่น) · ERP/CRP จาก Damodaran
ทุกค่าเก็บเป็น field = {value, source, url, fetched_at, asof} ถ้าหาไม่ได้ value เป็น null พร้อม reason ห้ามเดา
รูปแบบ attempt/clean/stmt_to_dict/fetch_th10y ดัดแปลงจาก AI investor alpha/data/fetch.py
ค่าคงที่ทั้งหมดอยู่ใน config.yaml
"""
from __future__ import annotations

import datetime as dt
import html
import io
import json
import math
import os
import re
import time
import warnings
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import yfinance as yf

from . import CFG, ROOT

# yfinance ยังใช้ inplace= ที่ pandas เตือนว่าเลิกใช้ ไม่กระทบผลลัพธ์ ปิดเฉพาะเสียงเตือนจาก yfinance กัน log ท่วม
# ต้องตั้งหลัง import yfinance เพราะตอน import มันแทรก filter 'default' ของตัวเองไว้หน้าสุด
warnings.filterwarnings("ignore", module=r"yfinance(\..*)?")

F = CFG["fetch"]
Y = CFG["yahoo"]
RF = CFG["risk_free"]
DM = CFG["damodaran"]
TZ = ZoneInfo(CFG["timezone"])
RAW_DIR = ROOT / CFG["paths"]["raw_dir"]
YF_SOURCE = Y["source_label"].format(version=yf.__version__)
SCHEMA_VERSION = 2   # เพิ่มเมื่อโครง JSON เปลี่ยน pipeline จะดึงใหม่เองถ้าไฟล์เก่ากว่านี้


# ---------- ตัวช่วยทั่วไป ----------

def now() -> dt.datetime:
    return dt.datetime.now(TZ)


def stamp(d: dt.datetime | None = None) -> str:
    return (d or now()).isoformat(timespec="seconds")


def write_json(path: Path, obj) -> None:
    """เขียนแบบ atomic: เขียนไฟล์ชั่วคราวก่อนแล้วค่อยเปลี่ยนชื่อ กันไฟล์พังเมื่อหยุดกลางคัน"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, allow_nan=False, indent=1)
    os.replace(tmp, path)


def clean(v):
    """ค่า NaN/NaT/inf -> None เสมอ (ไม่ใช่ 0), numpy -> python, วันที่ -> YYYY-MM-DD"""
    if v is None or v is pd.NaT:
        return None
    if isinstance(v, (pd.Timestamp, dt.datetime, dt.date)):
        return pd.Timestamp(v).strftime("%Y-%m-%d")
    if hasattr(v, "item") and not isinstance(v, (list, dict, str)):
        try:
            v = v.item()
        except Exception:
            pass
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


def attempt(fn, what: str):
    """รัน fn พร้อม retry ตาม config คืน (ผลลัพธ์, ข้อความ error หรือ None)"""
    last = None
    for i in range(F["retries"] + 1):
        try:
            return fn(), None
        except Exception as exc:  # noqa: BLE001
            last = f"{what}: {type(exc).__name__}: {exc}"[:300]
            if i < F["retries"]:
                time.sleep(F["backoff_seconds"][min(i, len(F["backoff_seconds"]) - 1)])
    return None, last


def http_get(url: str) -> requests.Response:
    r = requests.get(url, timeout=F["timeout_seconds"], headers={"User-Agent": F["user_agent"]})
    r.raise_for_status()
    return r


def field(value, source: str, url: str, asof: str | None = None, reason: str | None = None, **extra) -> dict:
    """ค่า 1 ค่าพร้อมที่มา ถ้า value เป็น None ต้องมี reason เสมอ"""
    value = clean(value)
    out = {"value": value, "source": source, "url": url, "fetched_at": stamp(), "asof": asof}
    if value is None:
        if not reason:
            raise ValueError(f"field ที่ไม่มีค่าต้องมี reason ({source})")
        out["reason"] = reason
    out.update(extra)
    return out


def get_info(t: yf.Ticker, what: str) -> tuple[dict, str | None]:
    """Ticker.info พร้อม retry คืน (info, error) ticker ที่ Yahoo ไม่รู้จักจะได้ dict ที่ไม่มี quoteType"""
    raw, err = attempt(t.get_info, what)
    if not err and not (raw or {}).get("quoteType"):
        err = f"{what}: Yahoo ไม่พบข้อมูล ticker นี้ (info ไม่มี quoteType)"
    return raw or {}, err


def yahoo_url(page: str, symbol: str) -> str:
    return Y["pages"][page].format(symbol=quote(symbol, safe=""))


def epoch_to_iso(ts, tz_name: str | None) -> str | None:
    if not isinstance(ts, (int, float)):
        return None
    return stamp(dt.datetime.fromtimestamp(ts, ZoneInfo(tz_name) if tz_name else TZ))


def epoch_to_date(ts) -> str | None:
    if not isinstance(ts, (int, float)):
        return None
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%d")


# ---------- 1) Yahoo Finance: info ----------

def fetch_info(t: yf.Ticker, symbol: str) -> dict:
    raw, err = get_info(t, "info")
    asof_by_kind = {
        "market_time": epoch_to_iso(raw.get("regularMarketTime"), raw.get("exchangeTimezoneName")),
        "mrq": epoch_to_date(raw.get("mostRecentQuarter")),
        "none": None,
    }
    asof_notes = {
        "market_time": "asof = regularMarketTime (เวลาราคาล่าสุดตามเขตเวลาตลาด)",
        "mrq": "asof = mostRecentQuarter เพราะหน้า Key Statistics แสดงค่านี้เป็น (mrq)",
        "none": "Yahoo ไม่ระบุวันที่ของค่านี้ เป็นค่าสด ณ fetched_at",
    }
    out = {}
    for name, spec in Y["info_fields"].items():
        url = yahoo_url(spec["page"], symbol)
        key = next((k for k in spec["keys"] if clean(raw.get(k)) is not None), None)
        if key is None:
            why = err or f"Yahoo ไม่มีค่า {' / '.join(spec['keys'])} สำหรับ {symbol}"
            out[name] = field(None, f"{YF_SOURCE} Ticker.info[{' | '.join(spec['keys'])}]", url, reason=why)
            continue
        asof = asof_by_kind[spec["asof"]]
        note = asof_notes[spec["asof"]] if asof or spec["asof"] == "none" else "Yahoo ไม่ให้เวลาอ้างอิงของค่านี้"
        out[name] = field(raw[key], f"{YF_SOURCE} Ticker.info['{key}']", url, asof=asof, asof_note=note)
    return out


# ---------- 2) Yahoo Finance: งบรายปีและปันผล ----------

def stmt_to_dict(df) -> dict | None:
    if df is None or df.empty:
        return None
    cols = [pd.Timestamp(c).strftime("%Y-%m-%d") for c in df.columns]
    items = {str(idx): {c: clean(v) for c, v in zip(cols, row.values)} for idx, row in df.iterrows()}
    return {"period_ends": cols, "items": items}


def fetch_statements(t: yf.Ticker, symbol: str) -> dict:
    out = {}
    for name, attr in Y["statements"].items():
        df, err = attempt(lambda: getattr(t, attr), name)
        sd = None if err else stmt_to_dict(df)
        src = f"{YF_SOURCE} Ticker.{attr} (งบรายปี)"
        url = yahoo_url(name, symbol)
        if sd is None:
            out[name] = field(None, src, url, reason=err or f"Yahoo ไม่มีงบ {name} ของ {symbol} (DataFrame ว่าง)")
        else:
            out[name] = field(
                sd, src, url, asof=sd["period_ends"][0],
                unit="หน่วยเต็มของ info.financial_currency ไม่แปลงหน่วย",
                asof_note="asof = งวดล่าสุด, period_ends เรียงจากใหม่ไปเก่า",
            )
    return out


def fetch_dividends(t: yf.Ticker, symbol: str) -> dict:
    src = f"{YF_SOURCE} Ticker.dividends"
    url = yahoo_url("dividends", symbol)
    s, err = attempt(lambda: t.dividends, "dividends")
    if err:
        return field(None, src, url, reason=err)
    rows = [
        {"ex_date": pd.Timestamp(d).strftime("%Y-%m-%d"), "dps": float(v)}
        for d, v in s.items()
        if clean(v) is not None and v > 0
    ]
    note = "DPS เป็นสกุล info.currency ตามที่ Yahoo ให้ (ปรับตามการแตกพาร์แล้ว)"
    if not rows:
        note += " · Yahoo ไม่มีประวัติปันผลของหุ้นนี้"
    return field(rows, src, url, asof=rows[-1]["ex_date"] if rows else None, note=note)


# ---------- 3) Risk-free rate ----------

def fetch_th10y() -> dict:
    tb = RF["thaibma"]
    src = f"{tb['source_label']} อายุ {tb['tenor_years']:g} ปี"
    avail, err = attempt(lambda: http_get(tb["avail_url"]).json(), "ThaiBMA avail")
    if err:
        return field(None, src, tb["avail_url"], reason=f"ดึงรายการวันที่ของ ThaiBMA ไม่ได้: {err}", market="TH")
    asof = str(avail[-1])[:10]
    url = tb["gov_url_template"].format(date=asof)
    curve, err = attempt(lambda: http_get(url).json().get("Curve") or [], "ThaiBMA curve")
    if err:
        return field(None, src, url, asof=asof, reason=f"ดึง yield curve ของ ThaiBMA ไม่ได้: {err}", market="TH")
    pts = [p for p in curve if abs(float(p["X"]) - tb["tenor_years"]) < 1e-9]
    if not pts:
        return field(None, src, url, asof=asof, reason=f"ไม่มีจุด X={tb['tenor_years']} ใน Curve ของวันที่ {asof}", market="TH")
    y = float(pts[0]["Y"])
    return field(
        y / tb["percent_divisor"], src, url, asof=asof, market="TH",
        unit="ทศนิยมต่อปี (0.02 = 2%)", raw=y, raw_unit="% ต่อปี", tenor_years=tb["tenor_years"],
    )


def fetch_us10y(country: str | None) -> dict:
    us = RF["us"]

    def history():
        h = yf.Ticker(us["symbol"]).history(period=us["history_period"])
        if h is None or h["Close"].dropna().empty:
            raise ValueError("ประวัติราคาว่าง")
        return h["Close"].dropna()

    close, err = attempt(history, f"{us['symbol']} history")
    extra = {"market": "US"}
    if country and country != us["home_country"]:
        extra["warning"] = f"บริษัทอยู่ {country} แต่ใช้ US 10Y เป็น Rf ตามกติกา อาจไม่ตรงสกุลเงินของกระแสเงินสด"
    if err:
        return field(None, us["source_label"], us["url"], reason=err, **extra)
    y = float(close.iloc[-1])
    return field(
        round(y / us["percent_divisor"], 6), us["source_label"], us["url"], asof=pd.Timestamp(close.index[-1]).strftime("%Y-%m-%d"),
        unit="ทศนิยมต่อปี (0.04 = 4%) ปัด 6 ตำแหน่ง", raw=y, raw_unit="% ต่อปี (ราคาปิดของ ^TNX)", tenor_years=10.0, **extra,
    )


def fetch_rf(symbol: str, country: str | None) -> dict:
    if symbol.endswith(RF["thai_suffix"]):
        return fetch_th10y()
    return fetch_us10y(country)


# ---------- 4) Damodaran: ERP และ country risk premium ----------

DAMODARAN_KEYS = ("erp_mature", "crp", "erp_country_total", "tax_rate_marginal", "moodys_rating", "default_spread")


def _cells(row_html: str) -> list[str]:
    tds = re.findall(r"<td[^>]*>(.*?)</td>", row_html, re.S | re.I)
    return [html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c))).strip() for c in tds]


def _pct(s: str) -> float | None:
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)%", s or "")
    return round(float(m.group(1)) / DM["percent_divisor"], 6) if m else None


def parse_ctryprem(page: str) -> tuple[dict, dict, str | None, str | None]:
    """คืน (ชื่อคอลัมน์ -> index, ชื่อประเทศ -> (cells, หมายเหตุของแถว), asof ISO, asof ตามต้นฉบับ)"""
    rows = [_cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", page, re.S | re.I)]
    cols = DM["columns"]
    header_i = next((i for i, c in enumerate(rows) if c and c[0] == cols["country"]), None)
    if header_i is None:
        raise ValueError(f"ไม่พบแถวหัวตารางที่ขึ้นต้นด้วย '{cols['country']}'")
    header = rows[header_i]
    missing = [v for v in cols.values() if v not in header]
    if missing:
        raise ValueError(f"ไม่พบคอลัมน์ {missing} ในหัวตาราง {header}")
    idx = {k: header.index(v) for k, v in cols.items()}
    table = {}
    for c in rows[header_i + 1:]:
        if not c or not c[0]:
            continue
        note = re.search(r"\((updated[^)]*)\)", c[0])
        name = re.sub(r"\s*\(updated[^)]*\)", "", c[0]).strip()
        table[name] = (c, note.group(1) if note else None)
    plain = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
    m = re.search(r"Last updated:\s*([A-Z][a-z]+ \d{1,2}, \d{4})", plain)
    asof = dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat() if m else None
    return idx, table, asof, m.group(1) if m else None


def fetch_damodaran(country: str | None) -> dict:
    url = DM["ctryprem_url"]
    src = DM["source_label"]

    def all_null(reason: str, asof: str | None = None) -> dict:
        return {k: field(None, src, url, asof=asof, reason=reason) for k in DAMODARAN_KEYS}

    if not country:
        return all_null("ไม่รู้ประเทศของบริษัท (Yahoo ไม่มี info.country) จึงเลือกแถวในตาราง Damodaran ไม่ได้")
    resp, err = attempt(lambda: http_get(url), "Damodaran ctryprem")
    if err:
        return all_null(f"ดึงตาราง Damodaran ไม่ได้: {err}")
    try:
        idx, table, asof, asof_raw = parse_ctryprem(resp.text)
    except ValueError as exc:
        return all_null(f"อ่านตาราง Damodaran ไม่ได้ (โครงหน้าเว็บอาจเปลี่ยน): {exc}")
    target = DM["country_aliases"].get(country, country)
    if target not in table:
        return all_null(f"ไม่พบประเทศ '{target}' (จาก info.country = '{country}') ในตาราง Damodaran", asof)

    cells, row_note = table[target]
    base = {"country": target, "page_last_updated": asof_raw}
    if row_note:
        base["row_note"] = row_note

    def col(key: str, as_pct: bool = True) -> dict:
        s = cells[idx[key]] if idx[key] < len(cells) else ""
        v = _pct(s) if as_pct else (s or None)
        cite = f"{src}, แถว '{target}' คอลัมน์ '{DM['columns'][key]}'"
        extra = {**base, "raw": s, **({"unit": "ทศนิยม (0.05 = 5%)"} if as_pct else {})}
        return field(v, cite, url, asof=asof, reason=f"ช่อง '{DM['columns'][key]}' ของ {target} เป็น '{s}'", **extra)

    crp = col("crp")
    erp_total = col("erp_total")
    mature = None
    if crp["value"] is not None and erp_total["value"] is not None:
        mature = round(erp_total["value"] - crp["value"], 6)
    erp_mature = field(
        mature,
        f"{src}, แถว '{target}': Equity Risk Premium − Country Risk Premium (คำนวณจากตารางเดียวกัน)",
        url, asof=asof, reason="ขาด Equity Risk Premium หรือ Country Risk Premium ของประเทศนี้",
        derived=True, unit="ทศนิยม (0.05 = 5%)", **base,
    )
    return {
        "erp_mature": erp_mature,
        "crp": crp,
        "erp_country_total": erp_total,
        "tax_rate_marginal": col("tax_rate"),
        "moodys_rating": col("rating", as_pct=False),
        "default_spread": col("default_spread"),
    }


def fetch_industry_beta(country: str | None, industry: str | None) -> dict:
    """unlevered beta ของอุตสาหกรรม (corrected for cash) จากไฟล์ Damodaran ตามภูมิภาคของบริษัท"""
    ib = DM["industry_beta"]
    url = ib["files"].get(country, ib["files"]["default"])
    region = ib["regions"].get(country, ib["regions"]["default"])
    src = f"{ib['source_label']} ({region}) คอลัมน์ '{ib['beta_column']}'"
    target = ib["industry_map"].get(industry)
    base = {"region": region, "yahoo_industry": industry}
    if not target:
        return field(None, src, url, reason=f"ยังไม่ได้จับคู่ Yahoo industry '{industry}' กับอุตสาหกรรมของ Damodaran "
                                             "(เพิ่มใน config.yaml damodaran.industry_beta.industry_map)", **base)
    resp, err = attempt(lambda: http_get(url), "Damodaran industry beta")
    if err:
        return field(None, src, url, reason=f"ดึงไฟล์ beta ของ Damodaran ไม่ได้: {err}", **base)
    try:
        df = pd.read_excel(io.BytesIO(resp.content), sheet_name=ib["sheet"], header=None, engine="calamine")
    except Exception as exc:  # noqa: BLE001
        return field(None, src, url, reason=f"อ่านไฟล์ beta ไม่ได้: {type(exc).__name__}: {exc}"[:300], **base)
    first = df.iloc[:, 0].astype(str).str.strip()
    asof = None
    date_rows = df[first == ib["date_label"]]
    if not date_rows.empty:
        asof = clean(date_rows.iloc[0, 1])
    head = first[first == ib["header_first_cell"]].index
    if head.empty:
        return field(None, src, url, asof=asof, reason=f"ไม่พบหัวตาราง '{ib['header_first_cell']}'", **base)
    header = [str(c).strip() for c in df.iloc[head[0]].tolist()]
    if ib["beta_column"] not in header:
        return field(None, src, url, asof=asof, reason=f"ไม่พบคอลัมน์ '{ib['beta_column']}'", **base)
    rows = df.iloc[head[0] + 1:]
    hit = rows[rows.iloc[:, 0].astype(str).str.strip() == target]
    if hit.empty:
        return field(None, src, url, asof=asof, reason=f"ไม่พบอุตสาหกรรม '{target}' ในไฟล์", **base)
    row = hit.iloc[0]
    return field(
        float(row.iloc[header.index(ib["beta_column"])]), f"{src}, แถว '{target}'", url, asof=asof,
        industry=target, n_firms=clean(row.iloc[header.index(ib["firms_column"])]), **base,
    )


def fetch_rating_table() -> dict:
    """ตาราง interest coverage -> synthetic rating -> default spread (บริษัทขนาดใหญ่ที่ไม่ใช่การเงิน)"""
    rt = DM["ratings"]
    url, src = rt["url"], rt["source_label"]
    resp, err = attempt(lambda: http_get(url), "Damodaran ratings")
    if err:
        return field(None, src, url, reason=f"ดึงตาราง rating ของ Damodaran ไม่ได้: {err}")
    rows = [_cells(r) for r in re.findall(r"<tr[^>]*>(.*?)</tr>", resp.text, re.S | re.I)]
    table = []
    for c in rows:
        if len(c) < 4:
            continue
        try:
            lo, hi = float(c[0]), float(c[1])
        except ValueError:
            continue
        spread = _pct(c[3])
        if spread is None:
            continue
        table.append({"coverage_gt": lo, "coverage_le": hi, "rating": c[2], "spread": spread})
    plain = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", resp.text)))
    m = re.search(rt["date_pattern"], plain)
    asof = dt.datetime.strptime(m.group(0), "%B %Y").date().isoformat() if m else None
    if not table:
        return field(None, src, url, asof=asof, reason="อ่านตาราง rating ไม่ได้ (โครงหน้าเว็บอาจเปลี่ยน)")
    return field(table, f"{src} (ตารางซ้าย: {rt['table_label']})", url, asof=asof,
                 asof_note="asof = เดือนที่หน้าเว็บระบุ (วันที่ 1 ของเดือน)", unit="spread เป็นทศนิยม")


# ---------- 5) Peers สำหรับ comps ----------

def fetch_peers(symbols: list[str]) -> dict:
    """ดึง multiple ของ peer แต่ละตัว คืน {symbol: {ชื่อฟิลด์: field}}"""
    out = {}
    for sym in symbols:
        raw, err = get_info(yf.Ticker(sym), f"peer {sym} info")
        url = yahoo_url("key_statistics", sym)
        market_time = epoch_to_iso(raw.get("regularMarketTime"), raw.get("exchangeTimezoneName"))
        entry = {}
        for name, key in Y["peer_context_fields"].items():
            entry[name] = field(raw.get(key), f"{YF_SOURCE} Ticker.info['{key}'] ของ {sym}", url,
                                reason=err or f"Yahoo ไม่มีค่า {key} สำหรับ {sym}")
        for name, key in Y["peer_fields"].items():
            entry[name] = field(raw.get(key), f"{YF_SOURCE} Ticker.info['{key}'] ของ {sym}", url, asof=market_time,
                                reason=err or f"Yahoo ไม่มีค่า {key} สำหรับ {sym}",
                                asof_note="asof = regularMarketTime ของ peer (multiple คิดจากราคาล่าสุด)")
        entry["ev_to_ebitda"] = peer_ev_to_ebitda(yf.Ticker(sym), sym, raw, err)
        out[sym] = entry
    return out


def _latest(sd: dict | None, item: str) -> tuple[float | None, str | None]:
    if not sd or item not in sd["items"]:
        return None, None
    return next(((sd["items"][item][p], p) for p in sd["period_ends"] if sd["items"][item].get(p) is not None),
                (None, None))


def peer_ev_to_ebitda(t: yf.Ticker, sym: str, info: dict, err: str | None) -> dict:
    """EV/EBITDA คิดเองจากงบรายปี นิยามเดียวกับบริษัทเป้าหมาย ไม่ใช้ enterpriseToEbitda ของ Yahoo
    เพราะ Yahoo ใช้ EBITDA ย้อนหลัง 12 เดือนที่ไม่ตรงกับงบรายปี (CPALL: 12.98 เทียบหน้าเว็บ 10.67)"""
    formula = "(marketCap + Total Debt + Minority Interest − Cash And Cash Equivalents) ÷ EBITDA งวดล่าสุดของงบรายปี"
    src = f"คำนวณจาก {YF_SOURCE} Ticker.info['marketCap'] และงบรายปี balance_sheet / income_stmt ของ {sym}: {formula}"
    url = yahoo_url("balance_sheet", sym)
    if err:
        return field(None, src, url, reason=err)
    cur, fin = info.get("currency"), info.get("financialCurrency")
    if cur != fin:
        return field(None, src, url, reason=f"ราคาเป็น {cur} แต่งบเป็น {fin} ต้องแปลงสกุลเงินก่อน จึงไม่คำนวณ")
    bs, e1 = attempt(lambda: stmt_to_dict(t.balance_sheet), f"peer {sym} balance_sheet")
    inc, e2 = attempt(lambda: stmt_to_dict(t.income_stmt), f"peer {sym} income_stmt")
    if e1 or e2:
        return field(None, src, url, reason=e1 or e2)
    mc = clean(info.get("marketCap"))
    debt, p_debt = _latest(bs, "Total Debt")
    cash, _ = _latest(bs, "Cash And Cash Equivalents")
    minority, _ = _latest(bs, "Minority Interest")
    ebitda, p_ebitda = _latest(inc, "EBITDA")
    missing = [n for n, v in (("marketCap", mc), ("Total Debt", debt), ("Cash And Cash Equivalents", cash),
                              ("EBITDA", ebitda)) if v is None]
    if missing:
        return field(None, src, url, reason=f"Yahoo ไม่มี {', '.join(missing)} ของ {sym}")
    if ebitda <= 0:
        return field(None, src, url, asof=p_ebitda, reason=f"EBITDA ของ {sym} ไม่เป็นบวก ({ebitda:,.0f})")
    ev = mc + debt + (minority or 0) - cash
    return field(round(ev / ebitda, 6), src, url, asof=p_ebitda,
                 asof_note="asof = งวดของ EBITDA · marketCap เป็นค่าล่าสุด",
                 components={"market_cap": mc, "total_debt": debt, "minority_interest": minority, "cash": cash,
                             "ebitda": ebitda, "balance_sheet_period": p_debt, "currency": cur},
                 note=None if minority is not None else "ไม่มีรายการ Minority Interest ในงบ นับเป็น 0")


# ---------- 6) รวมและตรวจ ----------

def fetch_ticker(symbol: str, peers: list[str], minority_proxy: str | None = None) -> dict:
    t = yf.Ticker(symbol)
    info = fetch_info(t, symbol)
    statements = fetch_statements(t, symbol)
    country = info["country"]["value"]

    notes = []
    cur, fin = info["currency"]["value"], info["financial_currency"]["value"]
    if cur and fin and cur != fin:
        notes.append(f"ราคาเป็น {cur} แต่งบเป็น {fin} ต้องแปลงสกุลก่อนคำนวณมูลค่าต่อหุ้น")
    for name, f in statements.items():
        if f["value"] and len(f["value"]["period_ends"]) < Y["min_statement_years"]:
            notes.append(f"{name} มีแค่ {len(f['value']['period_ends'])} ปี น้อยกว่า {Y['min_statement_years']} ปี")

    return {
        "schema_version": SCHEMA_VERSION,
        "ticker": symbol,
        "fetched_at": stamp(),
        "versions": {"yfinance": yf.__version__, "pandas": pd.__version__},
        "field_format": "ทุกค่าเป็น {value, source, url, fetched_at, asof}; value = null ต้องมี reason",
        "info": info,
        "statements": statements,
        "dividends": fetch_dividends(t, symbol),
        "risk_free": fetch_rf(symbol, country),
        "damodaran": {**fetch_damodaran(country),
                      "unlevered_beta": fetch_industry_beta(country, info["industry"]["value"]),
                      "rating_table": fetch_rating_table()},
        "minority_proxy": {
            "requested": minority_proxy,
            "data": fetch_peers([minority_proxy])[minority_proxy] if minority_proxy else None,
            "note": "บริษัทลูกที่จดทะเบียน ใช้ P/BV แปลง minority interest จาก book เป็นมูลค่าตลาด",
        },
        "peers": {
            "requested": peers,
            "data": fetch_peers(peers),
            "note": "รายชื่อ peer ต้องให้ผู้เรียนยืนยันก่อนใช้" if peers else "ยังไม่ได้ระบุ peer (ใส่ด้วย --peers หลังผู้เรียนยืนยันรายชื่อ)",
        },
        "notes": notes,
    }


def walk_fields(obj, path: str = ""):
    """ไล่หา field ทุกตัวใน payload คืน (path, field)"""
    if isinstance(obj, dict):
        if "value" in obj and "source" in obj:
            yield path, obj
            return
        for k, v in obj.items():
            yield from walk_fields(v, f"{path}.{k}" if path else k)


def provenance_gaps(payload: dict) -> list[str]:
    gaps = []
    for path, f in walk_fields(payload):
        miss = [k for k in ("source", "url", "fetched_at") if not f.get(k)]
        if f["value"] is None and not f.get("reason"):
            miss.append("reason")
        if miss:
            gaps.append(f"{path}: ขาด {', '.join(miss)}")
    return gaps


def latest_year_nulls(statements: dict) -> dict:
    """จำนวนรายการในงบที่งวดล่าสุดเป็น null (รายงานให้รู้ ไม่ได้เติมค่า)"""
    out = {}
    for name, f in statements.items():
        if f["value"]:
            latest = f["value"]["period_ends"][0]
            items = f["value"]["items"]
            out[name] = (sum(1 for v in items.values() if v.get(latest) is None), len(items), latest)
    return out


def main(ticker: str, peers: list[str], minority_proxy: str | None = None) -> int:
    symbol = ticker.strip().upper()
    peers = [p.strip().upper() for p in peers]
    minority_proxy = minority_proxy.strip().upper() if minority_proxy else None
    print(f"{stamp()} ดึง {symbol}" + (f" พร้อม peer {peers}" if peers else "")
          + (f" และ minority proxy {minority_proxy}" if minority_proxy else ""), flush=True)
    payload = fetch_ticker(symbol, peers, minority_proxy)
    path = RAW_DIR / f"{symbol}.json"
    write_json(path, payload)

    info = payload["info"]
    rf = payload["risk_free"]
    dm = payload["damodaran"]
    print(f"บันทึก {path.relative_to(ROOT)}")
    print(f"  ราคา {info['price']['value']} {info['currency']['value']} (ณ {info['price']['asof']}) · "
          f"shares {info['shares_outstanding']['value']} · beta {info['beta']['value']}")
    print(f"  Rf {rf['value']} ({rf['source']}, ณ {rf['asof']}) · ERP mature {dm['erp_mature']['value']} · "
          f"CRP {dm['crp']['value']} · ประเทศ {info['country']['value']}")
    for name, (n_null, n, latest) in latest_year_nulls(payload["statements"]).items():
        print(f"  {name} งวด {latest}: null {n_null}/{n} รายการ")
    nulls = [(p, f["reason"]) for p, f in walk_fields(payload) if f["value"] is None]
    print(f"  ฟิลด์ที่เป็น null: {len(nulls)}")
    for p, why in nulls:
        print(f"    - {p}: {why}")
    for n in payload["notes"] + ([rf["warning"]] if rf.get("warning") else []):
        print(f"  หมายเหตุ: {n}")
    gaps = provenance_gaps(payload)
    if gaps:
        print("  ขาดที่มา:\n    " + "\n    ".join(gaps))
        return 2
    return 1 if info["price"]["value"] is None else 0
