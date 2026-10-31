"""สมมติฐานของหุ้น 1 ตัว: assumptions/<TICKER>.yaml

draft() ร่างไฟล์จากข้อมูลดิบ (ค่าเฉลี่ยในอดีต + ค่าตั้งต้นใน config) ให้ผู้เรียนรีวิว
load() อ่านไฟล์แล้วแปลงทุกค่าเป็น Input ที่มีที่มาครบ ค่าไหนอ้าง {from: ...} จะดึงจาก data/raw/<TICKER>.json

รูปแบบค่า 1 ตัวในไฟล์ yaml:
  {from: info.price}                                  ค่าจาก fetch (มีที่มาในตัว)
  {from: {stmt: income_stmt, item: Total Revenue}}    งวดล่าสุดของงบที่ไม่เป็น null
  {from: {dividends: ttm}}                            DPS รวมย้อนหลัง dividend_ttm_days วัน
  {value: 0.18, source: ..., url: ..., asof: ..., note: ...}   ค่าที่คำนวณหรือผู้เรียนกำหนด
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field as dc_field
from pathlib import Path

import yaml

from . import CFG, ROOT

V = CFG["valuation"]
ASSUMPTIONS_DIR = ROOT / V["assumptions_dir"]

# ลำดับและคำอธิบายของทุก input (ใช้ทั้ง Excel ชีต Inputs และตารางสมมติฐานใน HTML)
SPEC = {
    # ข้อเท็จจริงจากตลาด
    "price":            ("ราคาหุ้นล่าสุด", "ต่อหุ้น"),
    "shares":           ("จำนวนหุ้นที่ออกจำหน่าย", "หุ้น"),
    "week52_low":       ("ราคาต่ำสุด 52 สัปดาห์", "ต่อหุ้น"),
    "week52_high":      ("ราคาสูงสุด 52 สัปดาห์", "ต่อหุ้น"),
    "beta":             ("Beta จาก regression ของ Yahoo", "เท่า"),
    "beta_unlevered":   ("Unlevered beta ของอุตสาหกรรม (corrected for cash)", "เท่า"),
    "rf":               ("อัตราผลตอบแทนพันธบัตรรัฐบาล 10 ปี (ก่อนหัก default spread)", "%"),
    "country_default_spread": ("Default spread ของประเทศ (จาก rating ของรัฐบาล)", "%"),
    "erp":              ("Equity risk premium รวม country risk", "%"),
    "tax_rate_marginal": ("อัตราภาษีนิติบุคคลตามกฎหมาย", "%"),
    # งบการเงินงวดล่าสุด
    "revenue_base":     ("รายได้งวดล่าสุด (ปีฐานของ DCF)", "สกุลงบ"),
    "ebitda_ltm":       ("EBITDA งวดล่าสุด", "สกุลงบ"),
    "eps_ltm":          ("EPS ย้อนหลัง 12 เดือน (TTM) ให้ตรงกับ trailing P/E ของ peer", "ต่อหุ้น"),
    "equity_book":      ("ส่วนของผู้ถือหุ้นบริษัทใหญ่", "สกุลงบ"),
    "total_debt":       ("หนี้สินที่มีภาระดอกเบี้ยรวม (รวม lease)", "สกุลงบ"),
    "lease_liabilities": ("หนี้สินตามสัญญาเช่า", "สกุลงบ"),
    "cash":             ("เงินสดและรายการเทียบเท่า", "สกุลงบ"),
    "minority_interest": ("ส่วนได้เสียที่ไม่มีอำนาจควบคุม (book)", "สกุลงบ"),
    "minority_pb":      ("P/BV ที่ใช้แปลง minority interest เป็นมูลค่าตลาด", "เท่า"),
    "non_operating_assets": ("สินทรัพย์ที่ไม่ใช่การดำเนินงาน (เงินลงทุนในบริษัทร่วม/JV, อสังหาฯ เพื่อการลงทุน) ที่ไม่ได้อยู่ใน EBIT",
                             "สกุลงบ"),
    "dps_ttm":          ("เงินปันผลต่อหุ้นย้อนหลัง 12 เดือน", "ต่อหุ้น"),
    # สมมติฐาน
    "beta_method":      ("Beta ที่ใช้: bottom_up (relever จากอุตสาหกรรม) หรือ regression", "วิธี"),
    "include_leases_in_debt": ("นับหนี้ lease เป็นหนี้ใน WACC และ net debt", "ใช่/ไม่"),
    "rf_adjust_default": ("หัก default spread ของประเทศออกจากพันธบัตรรัฐบาลเพื่อได้ Rf", "ใช่/ไม่"),
    "tax_rate":         ("อัตราภาษีจริงที่ใช้คิด NOPAT", "%"),
    "interest_coverage": ("Interest coverage (EBIT ÷ ดอกเบี้ยจ่าย) งวดล่าสุด", "เท่า"),
    "company_default_spread": ("Default spread ของบริษัท (synthetic rating)", "%"),
    "revenue_growth":   ("อัตราเติบโตของรายได้ต่อปี", "%"),
    "ebit_margin":      ("EBIT margin", "%"),
    "da_pct_revenue":   ("ค่าเสื่อมราคาต่อรายได้", "%"),
    "capex_pct_revenue": ("Capex ต่อรายได้", "%"),
    "nwc_pct_delta_revenue": ("เงินทุนหมุนเวียนที่เพิ่มต่อรายได้ที่เพิ่ม", "%"),
    "terminal_growth":  ("Terminal growth (DCF)", "%"),
    "terminal_roc":     ("ROC ช่วง terminal (ใช้คิด reinvestment = g ÷ ROC)", "%"),
    "ddm_growth":       ("อัตราเติบโตปันผลระยะยาว (DDM)", "%"),
}

# รายการในงบที่บางบริษัทไม่มี (เช่น ไม่มีบริษัทลูกที่มีผู้ถือหุ้นอื่น) ถ้าไม่มีในงบให้นับเป็น 0
ZERO_IF_MISSING = ("minority_interest", "lease_liabilities")

# input ที่ไฟล์สมมติฐานรุ่นก่อนไม่มี ถ้าไม่ระบุให้ใช้ค่านี้ (ไฟล์เดิมคำนวณได้ผลเท่าเดิม)
OPTIONAL = {
    "non_operating_assets": (0, "ไม่ได้ระบุในไฟล์สมมติฐาน จึงนับเป็น 0 (playbook §2: บวกเงินลงทุนในบริษัทอื่นและสินทรัพย์ที่ไม่ใช่การดำเนินงาน "
                                "เฉพาะเมื่อรายได้ของสินทรัพย์นั้นไม่อยู่ใน EBIT)"),
}

# ค่าที่ draft ดึงตรงจากข้อมูลดิบ
DIRECT = {
    "price": "info.price",
    "shares": "info.shares_outstanding",
    "week52_low": "info.week52_low",
    "week52_high": "info.week52_high",
    "beta": "info.beta",
    "beta_unlevered": "damodaran.unlevered_beta",
    "tax_rate_marginal": "damodaran.tax_rate_marginal",
    "rf": "risk_free",
    "country_default_spread": "damodaran.default_spread",
    "erp": "damodaran.erp_country_total",
    "revenue_base": {"stmt": "income_stmt", "item": "Total Revenue"},
    "ebitda_ltm": {"stmt": "income_stmt", "item": "EBITDA"},
    "eps_ltm": "info.trailing_eps",
    "equity_book": {"stmt": "balance_sheet", "item": "Stockholders Equity"},
    "total_debt": {"stmt": "balance_sheet", "item": "Total Debt"},
    "lease_liabilities": {"stmt": "balance_sheet", "item": "Capital Lease Obligations"},
    "cash": {"stmt": "balance_sheet", "item": "Cash And Cash Equivalents"},
    "minority_interest": {"stmt": "balance_sheet", "item": "Minority Interest"},
    "dps_ttm": {"dividends": "ttm"},
}


@dataclass
class Input:
    key: str
    value: object
    source: str
    url: str | None
    asof: str | None
    note: str | None = None
    kind: str = "fact"          # fact = จากแหล่งข้อมูล · derived = คำนวณจากแหล่งข้อมูล · assumption = ผู้เรียนกำหนด
    fetched_at: str | None = None

    @property
    def label(self) -> str:
        return SPEC[self.key][0]

    @property
    def unit(self) -> str:
        return SPEC[self.key][1]


@dataclass
class Assumptions:
    ticker: str
    status: str
    methods: list[str]
    peers: list[str]
    method_choice: str | None
    method_reasons: dict[str, str] = dc_field(default_factory=dict)
    limitations: list[str] = dc_field(default_factory=list)
    inputs: dict[str, Input] = dc_field(default_factory=dict)

    def __getitem__(self, key: str):
        return self.inputs[key].value


# ---------- อ่านค่าจากข้อมูลดิบ ----------

def latest(stmt_field: dict, item: str) -> tuple[object, str | None]:
    """ค่างวดล่าสุดที่ไม่เป็น null ของรายการในงบ คืน (ค่า, วันสิ้นงวด)"""
    sd = stmt_field["value"]
    if not sd or item not in sd["items"]:
        return None, None
    for period in sd["period_ends"]:
        v = sd["items"][item].get(period)
        if v is not None:
            return v, period
    return None, None


def series(raw: dict, stmt: str, item: str) -> dict[str, float]:
    """{วันสิ้นงวด: ค่า} เฉพาะงวดที่มีค่า เรียงเก่าไปใหม่"""
    sd = raw["statements"][stmt]["value"]
    if not sd or item not in sd["items"]:
        return {}
    vals = sd["items"][item]
    return {p: vals[p] for p in reversed(sd["period_ends"]) if vals.get(p) is not None}


def resolve(raw: dict, key: str, ref) -> Input:
    if isinstance(ref, str):
        f = raw
        for part in ref.split("."):
            f = f[part]
        return Input(key, f["value"], f["source"], f.get("url"), f.get("asof"),
                     note=f.get("reason") or f.get("asof_note"), fetched_at=f.get("fetched_at"))
    if "stmt" in ref:
        f = raw["statements"][ref["stmt"]]
        v, period = latest(f, ref["item"])
        reason = None if v is not None else f"ไม่มี '{ref['item']}' ใน {ref['stmt']}"
        return Input(key, v, f"{f['source']} รายการ '{ref['item']}'", f.get("url"), period,
                     note=reason, fetched_at=f.get("fetched_at"))
    if ref.get("dividends") == "ttm":
        f = raw["dividends"]
        rows = f["value"] or []
        cutoff = (dt.date.fromisoformat(raw["fetched_at"][:10]) - dt.timedelta(days=V["dividend_ttm_days"])).isoformat()
        recent = [r for r in rows if r["ex_date"] > cutoff]
        note = "XD ที่นับ: " + ", ".join(f"{r['ex_date']} ({r['dps']:g})" for r in recent) if recent else "ไม่มีปันผลใน 12 เดือนล่าสุด"
        return Input(key, round(sum(r["dps"] for r in recent), 6), f["source"], f.get("url"),
                     recent[-1]["ex_date"] if recent else None, note=note, fetched_at=f.get("fetched_at"))
    raise ValueError(f"{key}: ไม่รู้จักรูปแบบ from = {ref!r}")


# ---------- ร่างสมมติฐาน ----------

def _avg(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if len(xs) >= V["min_history_years"] else None


def _derived(raw: dict, stmt: str, value, how: str, periods: list[str]) -> dict:
    f = raw["statements"][stmt]
    span = f"{periods[0][:4]}–{periods[-1][:4]}" if periods else "ไม่มีงวดที่ใช้ได้"
    out = {"value": None if value is None else round(value, 6),
           "source": f"คำนวณจาก {f['source']} งวด {span}: {how}",
           "url": f.get("url"), "asof": periods[-1] if periods else None, "kind": "derived"}
    if value is None:
        out["note"] = f"ข้อมูลไม่พอ (ต้องมีอย่างน้อย {V['min_history_years']} ปี)"
    return out


def draft_inputs(raw: dict) -> dict:
    n = V["forecast_years"]
    rev = series(raw, "income_stmt", "Total Revenue")
    ebit = series(raw, "income_stmt", "EBIT")
    tax = series(raw, "income_stmt", "Tax Provision")
    pretax = series(raw, "income_stmt", "Pretax Income")
    interest = series(raw, "income_stmt", "Interest Expense")
    debt = series(raw, "balance_sheet", "Total Debt")
    equity = series(raw, "balance_sheet", "Stockholders Equity")
    minority = series(raw, "balance_sheet", "Minority Interest")
    cash = series(raw, "balance_sheet", "Cash And Cash Equivalents")
    invested = {p: equity[p] + minority.get(p, 0) + debt[p] - cash.get(p, 0)
                for p in equity if p in debt and equity[p] + minority.get(p, 0) + debt[p] - cash.get(p, 0) > 0}
    da = series(raw, "cash_flow", "Depreciation And Amortization")
    capex = series(raw, "cash_flow", "Capital Expenditure")
    dwc = series(raw, "cash_flow", "Change In Working Capital")

    out: dict = {k: {"from": ref} for k, ref in DIRECT.items()}
    for key in ZERO_IF_MISSING:
        ref = DIRECT[key]
        f = raw["statements"][ref["stmt"]]
        if latest(f, ref["item"])[0] is None:
            out[key] = {"value": 0, "source": f"{f['source']}: ไม่มีรายการ '{ref['item']}' ในงบ จึงนับเป็น 0",
                        "url": f.get("url"), "asof": f.get("asof"), "kind": "derived"}

    yrs = [p for p in pretax if p in tax and pretax[p] > 0]
    out["tax_rate"] = _derived(raw, "income_stmt", _avg([tax[p] / pretax[p] for p in yrs]),
                               "เฉลี่ย Tax Provision ÷ Pretax Income", yrs)

    # cost of debt = Rf + default spread จาก synthetic rating (playbook §3) ไม่ใช้ดอกเบี้ยจ่าย ÷ หนี้ตามบัญชี
    last = next((p for p in reversed(list(ebit)) if p in interest and interest[p] > 0), None)
    cov = ebit[last] / interest[last] if last else None
    ic = _derived(raw, "income_stmt", cov, "EBIT ÷ Interest Expense งวดล่าสุด", [last] if last else [])
    if cov is None:
        ic["note"] = "ไม่มี EBIT หรือดอกเบี้ยจ่ายงวดล่าสุด"
    out["interest_coverage"] = ic
    out["company_default_spread"] = synthetic_spread(raw, cov)

    roc_yrs = [p for p in ebit if p in tax and p in pretax and pretax[p] > 0 and p in invested]
    roc = _avg([ebit[p] * (1 - tax[p] / pretax[p]) / invested[p] for p in roc_yrs])
    tr = _derived(raw, "income_stmt", roc, "เฉลี่ย EBIT × (1 − Tax ÷ Pretax) ÷ (Stockholders Equity + Minority Interest "
                  "+ Total Debt − Cash) ของงวดเดียวกัน (balance_sheet)", roc_yrs)
    tr["note"] = "ROC ในอดีตใช้เป็นค่าตั้งต้นของ ROC ช่วง terminal (playbook §4: reinvestment = g ÷ ROC)"
    out["terminal_roc"] = tr

    rp = list(rev)
    cagr = (rev[rp[-1]] / rev[rp[0]]) ** (1 / (len(rp) - 1)) - 1 if len(rp) >= V["min_history_years"] else None
    g = _derived(raw, "income_stmt", cagr, "CAGR ของ Total Revenue (ใช้ค่าเดียวกันทุกปีที่ประมาณการ)", rp)
    g["value"] = None if cagr is None else [round(cagr, 6)] * n
    out["revenue_growth"] = g

    yrs = [p for p in rev if p in ebit]
    m = _avg([ebit[p] / rev[p] for p in yrs])
    em = _derived(raw, "income_stmt", m, "เฉลี่ย EBIT ÷ Total Revenue (ใช้ค่าเดียวกันทุกปีที่ประมาณการ)", yrs)
    em["value"] = None if m is None else [round(m, 6)] * n
    out["ebit_margin"] = em

    yrs = [p for p in rev if p in da]
    out["da_pct_revenue"] = _derived(raw, "cash_flow", _avg([da[p] / rev[p] for p in yrs]),
                                     "เฉลี่ย Depreciation And Amortization ÷ Total Revenue", yrs)
    yrs = [p for p in rev if p in capex]
    out["capex_pct_revenue"] = _derived(raw, "cash_flow", _avg([-capex[p] / rev[p] for p in yrs]),
                                        "เฉลี่ย −Capital Expenditure ÷ Total Revenue", yrs)
    pairs = [(a, b) for a, b in zip(rp, rp[1:]) if b in dwc and rev[b] != rev[a]]
    out["nwc_pct_delta_revenue"] = _derived(
        raw, "cash_flow", _avg([-dwc[b] / (rev[b] - rev[a]) for a, b in pairs]),
        "เฉลี่ย −Change In Working Capital ÷ รายได้ที่เพิ่มขึ้น", [b for _, b in pairs])

    proxy = (raw.get("minority_proxy") or {}).get("data")
    if proxy and proxy["price_to_book"]["value"]:
        out["minority_pb"] = {"from": "minority_proxy.data.price_to_book",
                              "note": f"P/BV ของบริษัทลูกที่จดทะเบียน {raw['minority_proxy']['requested']} "
                                      "(playbook §2: แปลง minority interest จาก book เป็น market)"}
    else:
        out["minority_pb"] = assumption(1.0, "ใช้ book value เพราะไม่ได้ระบุบริษัทลูกที่จดทะเบียน (minority_proxy)")

    for key, (value, source) in OPTIONAL.items():
        out[key] = assumption(value, source)

    dflt = V["draft_defaults"]
    for key in ("include_leases_in_debt", "beta_method"):
        out[key] = assumption(dflt[key], "ค่าตั้งต้นใน config.yaml ตาม research/playbook.md")
    cds = raw["damodaran"]["default_spread"]["value"] or 0
    out["rf_adjust_default"] = assumption(
        cds > 0, "research/playbook.md §3: ถ้าพันธบัตรรัฐบาลมี default risk ให้หัก country default spread ก่อนใช้เป็น Rf")
    rf_used = (raw["risk_free"]["value"] or 0) - (cds if cds > 0 else 0)
    for key in ("terminal_growth", "ddm_growth"):
        g = round(min(dflt[key], rf_used), 6)
        out[key] = assumption(g, f"research/playbook.md §4: g ต้องไม่เกิน Rf จึงใช้ค่าต่ำกว่าระหว่าง {dflt[key]:.2%} "
                                 f"(config.yaml) กับ Rf หลังหัก default spread {rf_used:.2%}")
    return out


def assumption(value, source: str) -> dict:
    return {"value": value, "source": source, "url": None, "asof": None, "kind": "assumption"}


def synthetic_spread(raw: dict, coverage: float | None) -> dict:
    f = raw["damodaran"]["rating_table"]
    out = {"value": None, "source": f["source"], "url": f["url"], "asof": f.get("asof"), "kind": "derived"}
    if coverage is None or not f["value"]:
        out["note"] = f.get("reason") or "ไม่มี interest coverage จึงหา rating ไม่ได้"
        return out
    row = next((r for r in f["value"] if r["coverage_gt"] < coverage <= r["coverage_le"]), None)
    if row is None:
        out["note"] = f"coverage {coverage:.2f} ไม่อยู่ในช่วงใดของตาราง"
        return out
    out["value"] = row["spread"]
    out["note"] = (f"coverage {coverage:.2f} อยู่ในช่วง > {row['coverage_gt']:g} ถึง ≤ {row['coverage_le']:g} "
                   f"→ rating {row['rating']}")
    return out


def draft(raw: dict) -> dict:
    return {
        "ticker": raw["ticker"],
        "status": "draft",
        "method_choice": f"research/{raw['ticker']}_method_choice.md",
        "methods": ["dcf_fcff", "ddm", "comps_pe", "comps_ev_ebitda", "comps_pb", "week52"],
        "method_reasons": {},
        "limitations": [],
        "peers": raw["peers"]["requested"],
        "minority_proxy": (raw.get("minority_proxy") or {}).get("requested"),
        "inputs": draft_inputs(raw),
    }


def path_for(ticker: str) -> Path:
    return ASSUMPTIONS_DIR / f"{ticker}.yaml"


def write_draft(raw: dict) -> Path:
    path = path_for(raw["ticker"])
    if path.exists():
        raise FileExistsError(f"{path.relative_to(ROOT)} มีอยู่แล้ว ไม่เขียนทับ (ลบเองถ้าต้องการร่างใหม่)")
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# สมมติฐานของ {raw['ticker']} ร่างจากข้อมูลดิบเมื่อ {raw['fetched_at']}\n"
        "# status: draft = ยังไม่ผ่านการรีวิว · reviewed = ผู้เรียนยืนยันแล้ว\n"
        "# ค่า kind: derived คำนวณจากอดีต · assumption ต้องอ้างเหตุผลจาก research/playbook.md ก่อนเปลี่ยน status\n"
    )
    path.write_text(header + yaml.safe_dump(draft(raw), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    return path


# ---------- อ่านสมมติฐาน ----------

def load(ticker: str, raw: dict) -> Assumptions:
    doc = yaml.safe_load(path_for(ticker).read_text(encoding="utf-8"))
    a = Assumptions(doc["ticker"], doc.get("status", "draft"), doc["methods"], doc.get("peers") or [],
                    doc.get("method_choice"), doc.get("method_reasons") or {}, doc.get("limitations") or [])
    unknown = set(doc["inputs"]) - set(SPEC)
    if unknown:
        raise ValueError(f"ไม่รู้จัก input: {sorted(unknown)}")
    for key in SPEC:
        entry = doc["inputs"].get(key)
        if entry is None and key in OPTIONAL:
            entry = assumption(*OPTIONAL[key])
        if entry is None:
            raise ValueError(f"{ticker}: ขาด input '{key}'")
        if "from" in entry:
            inp = resolve(raw, key, entry["from"])
            if entry.get("note"):
                inp.note = entry["note"]
        else:
            if not entry.get("source"):
                raise ValueError(f"{ticker}: input '{key}' ไม่มี source")
            inp = Input(key, entry["value"], entry["source"], entry.get("url"), entry.get("asof"),
                        note=entry.get("note"), kind=entry.get("kind", "assumption"))
        a.inputs[key] = inp
    missing = [f"{k} ({i.note or 'ไม่มีค่า'})" for k, i in a.inputs.items() if i.value is None]
    if missing:
        raise ValueError(f"{ticker}: input ที่ยังไม่มีค่า ต้องกำหนดเองใน {path_for(ticker).name}: " + "; ".join(missing))
    n = V["forecast_years"]
    for key in ("revenue_growth", "ebit_margin"):
        v = a.inputs[key].value
        if not isinstance(v, list) or len(v) != n:
            raise ValueError(f"{ticker}: '{key}' ต้องเป็น list ยาว {n} ปี (ได้ {v!r})")
    return a
