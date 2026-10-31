"""คำนวณมูลค่าต่อหุ้นทุกวิธีจาก Assumptions (Python เป็นต้นฉบับ Excel ต้องให้ผลตรงกัน)

ทุกวิธีคืน Result: ช่วง low/base/high สำหรับ football field และ steps ที่อธิบายทีละขั้นใน HTML
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import CFG
from .assumptions import Assumptions

V = CFG["valuation"]
S = V["sensitivity"]

LABELS = {
    "dcf_fcff": "DCF (FCFF)",
    "ddm": "Dividend Discount Model",
    "comps_pe": "Comps: P/E",
    "comps_ev_ebitda": "Comps: EV/EBITDA",
    "comps_pb": "Comps: P/BV",
    "week52": "ช่วงราคา 52 สัปดาห์",
}


@dataclass
class Step:
    label: str
    formula: str
    value: float | None
    unit: str = ""


@dataclass
class Result:
    key: str
    low: float | None = None
    base: float | None = None
    high: float | None = None
    skipped: str | None = None
    steps: list[Step] = field(default_factory=list)
    detail: dict = field(default_factory=dict)

    @property
    def label(self) -> str:
        return LABELS[self.key]


def percentile(xs: list[float], p: float) -> float:
    """แบบเดียวกับ Excel PERCENTILE.INC (linear interpolation)"""
    s = sorted(xs)
    k = (len(s) - 1) * p / 100
    lo = int(k)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


def offsets(n: int) -> list[float]:
    return [i for i in range(-n, n + 1)]


# ---------- WACC ----------

def debt_used(a: Assumptions) -> float:
    return a["total_debt"] if a["include_leases_in_debt"] else a["total_debt"] - a["lease_liabilities"]


def wacc(a: Assumptions) -> dict:
    e = a["price"] * a["shares"]
    d = debt_used(a)
    if a["beta_method"] == "bottom_up":
        beta = a["beta_unlevered"] * (1 + (1 - a["tax_rate_marginal"]) * d / e)
    elif a["beta_method"] == "regression":
        beta = a["beta"]
    else:
        raise ValueError(f"beta_method ต้องเป็น bottom_up หรือ regression (ได้ {a['beta_method']!r})")
    rf = rf_used(a)
    ke = rf + beta * a["erp"]
    kd = rf + a["country_default_spread"] + a["company_default_spread"]
    kd_at = kd * (1 - a["tax_rate_marginal"])
    we, wd = e / (e + d), d / (e + d)
    return {"rf": rf, "beta": beta, "de": d / e, "ke": ke, "kd": kd, "kd_after_tax": kd_at, "equity_value_mkt": e,
            "debt": d, "we": we, "wd": wd, "wacc": we * ke + wd * kd_at}


def rf_used(a: Assumptions) -> float:
    """Rf ที่ไม่มี default risk: พันธบัตรรัฐบาล − country default spread (playbook §3)"""
    return a["rf"] - a["country_default_spread"] if a["rf_adjust_default"] else a["rf"]


def rate_steps(a: Assumptions, w: dict) -> list[Step]:
    """Rf → beta → Ke ใช้ร่วมกันทั้ง DCF และ DDM"""
    rf = [Step("Risk-free rate", "พันธบัตรรัฐบาล − country default spread", w["rf"], "%")] \
        if a["rf_adjust_default"] else [Step("Risk-free rate", "พันธบัตรรัฐบาล 10 ปี", w["rf"], "%")]
    if a["beta_method"] == "regression":
        beta = [Step("Beta (regression จาก Yahoo)", "Yahoo beta", w["beta"], "beta")]
    else:
        beta = [Step("D/E ตามมูลค่าตลาด", "หนี้ ÷ (ราคา × จำนวนหุ้น)", w["de"], "x"),
                Step("Levered beta (bottom-up)", "βu × (1 + (1 − tax marginal) × D/E)", w["beta"], "beta")]
    return [*rf, *beta, Step("Cost of equity (CAPM)", "Rf + Beta × ERP", w["ke"], "%")]


# ---------- DCF (FCFF) ----------

def forecast(a: Assumptions) -> list[dict]:
    rows, prev = [], a["revenue_base"]
    for t, (g, m) in enumerate(zip(a["revenue_growth"], a["ebit_margin"]), start=1):
        rev = prev * (1 + g)
        ebit = rev * m
        nopat = ebit * (1 - a["tax_rate"])
        da = rev * a["da_pct_revenue"]
        capex = rev * a["capex_pct_revenue"]
        dnwc = (rev - prev) * a["nwc_pct_delta_revenue"]
        rows.append({"t": t, "revenue": rev, "ebit": ebit, "nopat": nopat, "da": da, "capex": capex,
                     "dnwc": dnwc, "fcff": nopat + da - capex - dnwc})
        prev = rev
    return rows


def minority_market(a: Assumptions) -> float:
    return a["minority_interest"] * a["minority_pb"]


def equity_bridge(a: Assumptions) -> float:
    """EV -> มูลค่าส่วนของผู้ถือหุ้นบริษัทใหญ่: หักหนี้ บวกเงินสดและสินทรัพย์ที่ไม่ใช่การดำเนินงาน
    หัก minority interest ตามมูลค่าตลาด (playbook §2)"""
    return -debt_used(a) + a["cash"] + a["non_operating_assets"] - minority_market(a)


def terminal_roc(a: Assumptions, w: float) -> float:
    """terminal_roc = "wacc" แปลว่าไม่มี excess return ในช่วง terminal (playbook §4) ROC จึงเปลี่ยนตาม WACC"""
    return w if a["terminal_roc"] == "wacc" else a["terminal_roc"]


def terminal_fcff(a: Assumptions, fc: list[dict], g: float, w: float) -> float:
    """FCFF ปี n+1 = NOPATₙ × (1 + g) × (1 − g ÷ ROC) ให้ reinvestment สอดคล้องกับ g (playbook §4)"""
    return fc[-1]["nopat"] * (1 + g) * (1 - g / terminal_roc(a, w))


def dcf_per_share(a: Assumptions, fc: list[dict], w: float, g: float) -> float | None:
    if w <= g:
        return None
    n = len(fc)
    pv = sum(r["fcff"] / (1 + w) ** r["t"] for r in fc)
    tv = terminal_fcff(a, fc, g, w) / (w - g)
    return (pv + tv / (1 + w) ** n + equity_bridge(a)) / a["shares"]


def grid(fn, base_x: float, step_x: float, base_y: float, step_y: float, n: int) -> list[list[float | None]]:
    """ตาราง fn(x, y) แถว = x (WACC/ke), คอลัมน์ = y (growth)"""
    return [[fn(base_x + i * step_x, base_y + j * step_y) for j in offsets(n)] for i in offsets(n)]


def box_range(table: list[list[float | None]], k: int) -> tuple[float | None, float | None]:
    c = len(table) // 2
    vals = [v for row in table[c - k:c + k + 1] for v in row[c - k:c + k + 1] if v is not None]
    return (min(vals), max(vals)) if vals else (None, None)


def dcf(a: Assumptions, w: dict) -> Result:
    r = Result("dcf_fcff")
    fc = forecast(a)
    g = a["terminal_growth"]
    base = dcf_per_share(a, fc, w["wacc"], g)
    if base is None:
        r.skipped = f"WACC {w['wacc']:.2%} ไม่มากกว่า terminal growth {g:.2%} คำนวณ terminal value ไม่ได้"
        return r
    n = len(fc)
    pv_fcff = sum(x["fcff"] / (1 + w["wacc"]) ** x["t"] for x in fc)
    tv = terminal_fcff(a, fc, g, w["wacc"]) / (w["wacc"] - g)
    pv_tv = tv / (1 + w["wacc"]) ** n
    ev = pv_fcff + pv_tv
    table = grid(lambda x, y: dcf_per_share(a, fc, x, y), w["wacc"], S["wacc_step"], g, S["growth_step"], S["grid"])
    r.low, r.high = box_range(table, S["range_k"])
    r.base = base
    r.detail = {"forecast": fc, "pv_fcff": pv_fcff, "fcff_terminal": terminal_fcff(a, fc, g, w["wacc"]),
                "terminal_roc": terminal_roc(a, w["wacc"]), "tv": tv,
                "pv_tv": pv_tv, "ev": ev, "minority_market": minority_market(a),
                "tv_share": pv_tv / ev, "table": table,
                "x_axis": [w["wacc"] + i * S["wacc_step"] for i in offsets(S["grid"])],
                "y_axis": [g + j * S["growth_step"] for j in offsets(S["grid"])]}
    r.steps = [
        *rate_steps(a, w),
        Step("Cost of debt ก่อนภาษี", "Rf + country default spread + company default spread", w["kd"], "%"),
        Step("Cost of debt หลังภาษี", "Kd × (1 − tax marginal)", w["kd_after_tax"], "%"),
        Step("สัดส่วนทุน E/(D+E)", "ราคา × จำนวนหุ้น ÷ (มูลค่าตลาดทุน + หนี้)", w["we"], "%"),
        Step("WACC", "We × Ke + Wd × Kd หลังภาษี", w["wacc"], "%"),
        Step(f"FCFF ปีที่ {n}", "NOPAT + D&A − Capex − ΔNWC", fc[-1]["fcff"], "money"),
        Step("PV ของ FCFF ปี 1–%d" % n, "Σ FCFFₜ ÷ (1 + WACC)ᵗ", pv_fcff, "money"),
        Step(f"FCFF ปีที่ {n + 1}", f"NOPAT{n} × (1 + g) × (1 − g ÷ ROC)", r.detail["fcff_terminal"], "money"),
        Step("Terminal value", f"FCFF{n + 1} ÷ (WACC − g)", tv, "money"),
        Step("PV ของ terminal value", f"TV ÷ (1 + WACC)^{n}", pv_tv, "money"),
        Step("Enterprise value", "PV FCFF + PV TV", ev, "money"),
        Step("Minority interest ตามมูลค่าตลาด", "minority (book) × P/BV", minority_market(a), "money"),
        Step("หักหนี้ บวกเงินสด บวกสินทรัพย์ที่ไม่ใช่การดำเนินงาน หัก minority",
             "− หนี้ + เงินสด + สินทรัพย์ที่ไม่ใช่การดำเนินงาน − minority (market)", equity_bridge(a), "money"),
        Step("มูลค่าต่อหุ้น", "(EV − หนี้ + เงินสด + สินทรัพย์ที่ไม่ใช่การดำเนินงาน − minority) ÷ จำนวนหุ้น", base,
             "per_share"),
    ]
    return r


# ---------- DDM ----------

def ddm_per_share(d0: float, ke: float, g: float) -> float | None:
    return d0 * (1 + g) / (ke - g) if ke > g else None


def ddm(a: Assumptions, w: dict) -> Result:
    r = Result("ddm")
    d0, g, ke = a["dps_ttm"], a["ddm_growth"], w["ke"]
    if not d0:
        r.skipped = "ไม่มีเงินปันผลใน 12 เดือนล่าสุด"
        return r
    base = ddm_per_share(d0, ke, g)
    if base is None:
        r.skipped = f"Cost of equity {ke:.2%} ไม่มากกว่าอัตราเติบโตปันผล {g:.2%} ใช้ Gordon growth ไม่ได้"
        return r
    table = grid(lambda x, y: ddm_per_share(d0, x, y), ke, S["wacc_step"], g, S["growth_step"], S["grid"])
    r.low, r.high = box_range(table, S["range_k"])
    r.base = base
    r.detail = {"table": table, "x_axis": [ke + i * S["wacc_step"] for i in offsets(S["grid"])],
                "y_axis": [g + j * S["growth_step"] for j in offsets(S["grid"])]}
    r.steps = [
        Step("DPS ย้อนหลัง 12 เดือน (D₀)", "รวมเงินปันผลที่ XD ใน 12 เดือน", d0, "per_share"),
        Step("DPS ปีหน้า (D₁)", "D₀ × (1 + g)", d0 * (1 + g), "per_share"),
        *rate_steps(a, w),
        Step("มูลค่าต่อหุ้น", "D₁ ÷ (Ke − g)", base, "per_share"),
    ]
    return r


# ---------- Comps ----------

def bridge_book(a: Assumptions) -> float:
    """EV ของ peer รวม minority interest ตาม book จึงหักกลับด้วย book เพื่อให้นิยามเดียวกัน (ต่างจาก DCF ที่ใช้มูลค่าตลาด)"""
    return -debt_used(a) + a["cash"] - a["minority_interest"]


def target_multiples(a: Assumptions) -> dict:
    """ตัวคูณปัจจุบันของบริษัทเป้าหมาย คิดแบบเดียวกับ peer ใช้เทียบกับช่วงของ peer"""
    mc = a["price"] * a["shares"]
    return {"trailing_pe": a["price"] / a["eps_ltm"] if a["eps_ltm"] else None,
            "ev_to_ebitda": (mc - bridge_book(a)) / a["ebitda_ltm"] if a["ebitda_ltm"] else None,
            "price_to_book": mc / a["equity_book"] if a["equity_book"] else None}


MULTIPLE_NAMES = {"trailing_pe": "P/E (TTM)", "ev_to_ebitda": "EV/EBITDA", "price_to_book": "P/BV"}

COMPS = {
    # key: (ฟิลด์ multiple ของ peer, ฟังก์ชันแปลง multiple เป็นราคาต่อหุ้น, คำอธิบายสูตร)
    "comps_pe": ("trailing_pe", lambda a, m: m * a["eps_ltm"], "P/E × EPS (TTM)"),
    "comps_pb": ("price_to_book", lambda a, m: m * a["equity_book"] / a["shares"], "P/BV × (ส่วนผู้ถือหุ้น ÷ จำนวนหุ้น)"),
    "comps_ev_ebitda": ("ev_to_ebitda", lambda a, m: (m * a["ebitda_ltm"] + bridge_book(a)) / a["shares"],
                        "(EV/EBITDA × EBITDA − หนี้ + เงินสด − minority ตาม book) ÷ จำนวนหุ้น"),
}


def comps(a: Assumptions, key: str, peers_data: dict) -> Result:
    r = Result(key)
    fld, to_price, formula = COMPS[key]
    used = {s: d[fld]["value"] for s, d in peers_data.items() if s in a.peers and (d[fld]["value"] or 0) > 0}
    dropped = {s: (d[fld].get("reason") or "ค่าติดลบหรือเป็นศูนย์") for s, d in peers_data.items()
               if s in a.peers and s not in used}
    r.detail = {"field": fld, "used": used, "dropped": dropped, "target": target_multiples(a)[fld]}
    if key == "comps_pe" and a["eps_ltm"] <= 0:
        r.skipped = f"EPS (TTM) {a['eps_ltm']:g} ไม่เป็นบวก P/E ใช้กับบริษัทขาดทุนไม่ได้ (playbook §9)"
        return r
    if len(used) < 2:
        r.skipped = f"peer ที่มีค่า {fld} ใช้ได้มีแค่ {len(used)} ตัว (ต้องมีอย่างน้อย 2)" if a.peers else "ยังไม่ได้ยืนยันรายชื่อ peer"
        return r
    lo_p, mid_p, hi_p = V["comps_percentiles"]
    ms = [percentile(list(used.values()), p) for p in (lo_p, mid_p, hi_p)]
    r.low, r.base, r.high = (to_price(a, m) for m in ms)
    r.detail["multiples"] = ms
    r.steps = [
        Step(f"Multiple ของ peer P{lo_p} / P{mid_p} / P{hi_p}", "PERCENTILE ของ peer ที่ใช้ได้", None),
        *[Step(f"P{p} ของ peer", f"PERCENTILE.INC ของ {MULTIPLE_NAMES[fld]} ที่ {p}%", m, "x")
          for p, m in zip((lo_p, mid_p, hi_p), ms)],
        Step("มูลค่าต่อหุ้นที่ P%d" % mid_p, formula, r.base, "per_share"),
    ]
    return r


# ---------- 52 สัปดาห์ ----------

def week52(a: Assumptions) -> Result:
    r = Result("week52", low=a["week52_low"], high=a["week52_high"])
    r.steps = [Step("ต่ำสุด", "Yahoo fiftyTwoWeekLow", r.low, "per_share"),
               Step("สูงสุด", "Yahoo fiftyTwoWeekHigh", r.high, "per_share")]
    return r


def run(a: Assumptions, peers_data: dict) -> dict:
    w = wacc(a)
    results = []
    for key in a.methods:
        if key == "dcf_fcff":
            results.append(dcf(a, w))
        elif key == "ddm":
            results.append(ddm(a, w))
        elif key in COMPS:
            results.append(comps(a, key, peers_data))
        elif key == "week52":
            results.append(week52(a))
        else:
            raise ValueError(f"ไม่รู้จักวิธี {key}")
    return {"wacc": w, "results": results, "warnings": warnings(a, w, results)}


def warnings(a: Assumptions, w: dict, results: list[Result]) -> list[str]:
    """สมมติฐานที่ขัดกับกฎใน research/playbook.md (แสดงในรายงาน ไม่หยุดการคำนวณ)"""
    out = []
    for key, label in (("terminal_growth", "Terminal growth"), ("ddm_growth", "อัตราเติบโตปันผล")):
        if a[key] > w["rf"] + 1e-6:
            out.append(f"{label} {a[key]:.2%} สูงกว่า Rf {w['rf']:.2%} ขัดกับ playbook §4 (g ไม่ควรเกิน Rf)")
    if terminal_roc(a, w["wacc"]) < w["wacc"]:
        out.append(f"ROC ช่วง terminal {terminal_roc(a, w['wacc']):.2%} ต่ำกว่า WACC {w['wacc']:.2%} "
                   "การเติบโตจึงทำลายมูลค่า (playbook §4: excess return ควรเข้าหา 0)")
    for r in results:
        if r.key == "dcf_fcff" and not r.skipped:
            out.append(f"Terminal value เป็น {r.detail['tv_share']:.0%} ของ EV ผลอ่อนไหวกับ WACC และ g มาก "
                       "(playbook §4: ไม่พบกฎสัดส่วนใน notebook มีแค่ตัวอย่าง 46–70%)")
    return out
