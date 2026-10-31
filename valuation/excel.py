"""สร้าง output/<TICKER>/<TICKER>_valuation.xlsx ด้วย openpyxl

ทุกตัวเลขที่คำนวณเป็นสูตร Excel อ้างชีต Inputs ผ่าน defined name (in_*) แก้สมมติฐานในชีต Inputs แล้วทุกชีตคำนวณใหม่
สูตรต้องให้ผลตรงกับ methods.py (ตรวจด้วย verify.py)
"""
from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import absolute_coordinate, get_column_letter
from openpyxl.workbook.defined_name import DefinedName

from . import CFG
from .assumptions import Assumptions, SPEC, series
from .methods import COMPS, LABELS, offsets

V = CFG["valuation"]
S = V["sensitivity"]
N = V["forecast_years"]

BLUE = Font(color="1F4E9E")             # ค่าที่เป็น input (แก้ได้)
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=14)
HEAD = PatternFill("solid", fgColor="DCE6F1")
KEY = PatternFill("solid", fgColor="FFF2CC")
THIN = Border(bottom=Side(style="thin", color="999999"))
WRAP = Alignment(wrap_text=True, vertical="top")

FMT = {"%": "0.00%", "money": '#,##0,,"M"', "per_share": "#,##0.00", "x": "0.00",
       "หุ้น": "#,##0", "ต่อหุ้น": "#,##0.00", "เท่า": "0.000", "สกุลงบ": '#,##0,,"M"'}
PERIOD_INPUTS = ("revenue_growth", "ebit_margin")


def name(wb: Workbook, nm: str, sheet: str, cell: str) -> None:
    wb.defined_names[nm] = DefinedName(nm, attr_text=f"'{sheet}'!{absolute_coordinate(cell)}")


def abs_ref(col: int, row: int) -> str:
    return f"${get_column_letter(col)}${row}"


def header(ws, row: int, labels: list[str]) -> None:
    for c, text in enumerate(labels, start=1):
        cell = ws.cell(row, c, text)
        cell.font, cell.fill, cell.border = BOLD, HEAD, THIN


def widths(ws, ws_widths: dict[str, int]) -> None:
    for col, w in ws_widths.items():
        ws.column_dimensions[col].width = w


# ---------- Inputs ----------

def sheet_inputs(wb: Workbook, a: Assumptions) -> None:
    ws = wb.create_sheet("Inputs")
    ws["A1"], ws["A1"].font = f"Inputs · {a.ticker} · สถานะสมมติฐาน: {a.status}", TITLE
    ws["A2"] = "ตัวสีน้ำเงินคือค่าที่แก้ได้ ทุกชีตคำนวณจากค่าเหล่านี้ · ประเภท: fact = จากแหล่งข้อมูล, derived = คำนวณจากอดีต, assumption = ผู้เรียนกำหนด"
    header(ws, 4, ["key", "รายการ", "ค่า", "หน่วย", "ประเภท", "แหล่งที่มา", "URL", "ข้อมูล ณ", "หมายเหตุ"])
    r = 5
    for key in SPEC:
        inp = a.inputs[key]
        values = [(f"{key}_y{i}", f"{inp.label} ปีที่ {i}", v) for i, v in enumerate(inp.value, 1)] \
            if key in PERIOD_INPUTS else [(key, inp.label, inp.value)]
        for k, label, v in values:
            ws.cell(r, 1, k)
            ws.cell(r, 2, label)
            c = ws.cell(r, 3, v)
            c.font = BLUE
            c.number_format = FMT.get(inp.unit, "General")
            ws.cell(r, 4, inp.unit)
            ws.cell(r, 5, inp.kind)
            ws.cell(r, 6, inp.source).alignment = WRAP
            ws.cell(r, 7, inp.url)
            ws.cell(r, 8, inp.asof)
            ws.cell(r, 9, inp.note).alignment = WRAP
            name(wb, f"in_{k}", "Inputs", f"C{r}")
            r += 1
    widths(ws, {"A": 26, "B": 44, "C": 18, "D": 10, "E": 11, "F": 60, "G": 40, "H": 24, "I": 50})
    ws.freeze_panes = "C5"


# ---------- Historical ----------

HIST_ITEMS = [
    ("income_stmt", "Total Revenue"), ("income_stmt", "EBIT"), ("income_stmt", "EBITDA"),
    ("income_stmt", "Pretax Income"), ("income_stmt", "Tax Provision"), ("income_stmt", "Interest Expense"),
    ("income_stmt", "Net Income Common Stockholders"), ("income_stmt", "Diluted EPS"),
    ("balance_sheet", "Total Debt"), ("balance_sheet", "Capital Lease Obligations"),
    ("balance_sheet", "Cash And Cash Equivalents"), ("balance_sheet", "Stockholders Equity"),
    ("balance_sheet", "Minority Interest"),
    ("cash_flow", "Operating Cash Flow"), ("cash_flow", "Capital Expenditure"),
    ("cash_flow", "Depreciation And Amortization"), ("cash_flow", "Change In Working Capital"),
    ("cash_flow", "Free Cash Flow"),
]


def sheet_historical(wb: Workbook, raw: dict) -> None:
    ws = wb.create_sheet("Historical")
    ws["A1"], ws["A1"].font = "งบการเงินย้อนหลัง (Yahoo Finance งบรายปี)", TITLE
    periods = sorted({p for st, it in HIST_ITEMS for p in series(raw, st, it)})
    header(ws, 3, ["งบ", "รายการ", *periods, "แหล่งที่มา", "URL"])
    for r, (st, it) in enumerate(HIST_ITEMS, start=4):
        vals = series(raw, st, it)
        ws.cell(r, 1, st)
        ws.cell(r, 2, it)
        for c, p in enumerate(periods, start=3):
            cell = ws.cell(r, c, vals.get(p))
            cell.number_format = "0.00" if it == "Diluted EPS" else FMT["money"]
        f = raw["statements"][st]
        ws.cell(r, 3 + len(periods), f["source"])
        ws.cell(r, 4 + len(periods), f["url"])
    ws.cell(5 + len(HIST_ITEMS), 1, "งวดที่ Yahoo ไม่มีค่าเว้นว่างไว้ ไม่เติมเอง · หน่วย M = ล้าน (สกุลเงินตามงบ)")
    widths(ws, {"A": 14, "B": 34})


# ---------- WACC ----------

def sheet_wacc(wb: Workbook) -> None:
    ws = wb.create_sheet("WACC")
    ws["A1"], ws["A1"].font = "WACC", TITLE
    header(ws, 3, ["รายการ", "ค่า", "สูตร"])
    rows = [
        ("x_E", "มูลค่าตลาดของทุน (E)", "=in_price*in_shares", "money", "ราคา × จำนวนหุ้น"),
        ("x_debt", "หนี้ที่ใช้ (D)", "=IF(in_include_leases_in_debt,in_total_debt,in_total_debt-in_lease_liabilities)",
         "money", "หนี้รวม (หัก lease ถ้า include_leases_in_debt = FALSE)"),
        ("x_de", "D/E", "=x_debt/x_E", "x", "D ÷ E"),
        ("x_beta", "Beta ที่ใช้", '=IF(in_beta_method="bottom_up",in_beta_unlevered*(1+(1-in_tax_rate_marginal)*x_de),in_beta)',
         "x", "bottom_up: βu × (1 + (1 − tax marginal) × D/E) · regression: Yahoo beta"),
        ("x_rf", "Risk-free rate ที่ใช้", "=IF(in_rf_adjust_default,in_rf-in_country_default_spread,in_rf)", "%",
         "พันธบัตรรัฐบาล − country default spread (ถ้า rf_adjust_default = TRUE)"),
        ("x_ke", "Cost of equity (Ke)", "=x_rf+x_beta*in_erp", "%", "Rf + β × ERP"),
        ("x_kd_pre", "Cost of debt ก่อนภาษี", "=x_rf+in_country_default_spread+in_company_default_spread", "%",
         "Rf + country default spread + company default spread (synthetic rating)"),
        ("x_kd", "Cost of debt หลังภาษี", "=x_kd_pre*(1-in_tax_rate_marginal)", "%", "Kd × (1 − tax marginal)"),
        ("x_we", "We", "=x_E/(x_E+x_debt)", "%", "E ÷ (D + E)"),
        ("x_wd", "Wd", "=x_debt/(x_E+x_debt)", "%", "D ÷ (D + E)"),
        ("x_wacc", "WACC", "=x_we*x_ke+x_wd*x_kd", "%", "We × Ke + Wd × Kd หลังภาษี"),
        ("x_roc", "ROC ช่วง terminal", "=IF(ISNUMBER(in_terminal_roc),in_terminal_roc,x_wacc)", "%",
         'terminal_roc = "wacc" แปลว่า ROC = WACC (ไม่มี excess return)'),
        ("x_minority", "Minority interest ตามมูลค่าตลาด", "=in_minority_interest*in_minority_pb", "money",
         "minority (book) × P/BV"),
        ("x_bridge", "EV → Equity (− หนี้ + เงินสด − minority)", "=-x_debt+in_cash-x_minority", "money",
         "ใช้ทั้ง DCF และ EV/EBITDA"),
    ]
    for r, (nm, label, formula, unit, note) in enumerate(rows, start=4):
        ws.cell(r, 1, label)
        c = ws.cell(r, 2, formula)
        c.number_format = FMT[unit]
        ws.cell(r, 3, note)
        name(wb, nm, "WACC", f"B{r}")
        if nm == "x_wacc":
            c.fill = KEY
    widths(ws, {"A": 40, "B": 18, "C": 70})


# ---------- DCF ----------

DCF_ROWS = ["t", "growth", "revenue", "margin", "ebit", "nopat", "da", "capex", "dnwc", "fcff", "df", "pv"]


def sheet_dcf(wb: Workbook) -> dict[str, int]:
    ws = wb.create_sheet("DCF")
    ws["A1"], ws["A1"].font = "DCF (FCFF)", TITLE
    row = {k: 4 + i for i, k in enumerate(DCF_ROWS)}
    labels = {"t": "ปีที่", "growth": "การเติบโตของรายได้", "revenue": "รายได้", "margin": "EBIT margin",
              "ebit": "EBIT", "nopat": "NOPAT = EBIT × (1 − tax)", "da": "D&A", "capex": "Capex",
              "dnwc": "ΔNWC", "fcff": "FCFF = NOPAT + D&A − Capex − ΔNWC", "df": "Discount factor 1/(1+WACC)^t",
              "pv": "PV ของ FCFF"}
    for k, r in row.items():
        ws.cell(r, 1, labels[k])
    ws.cell(3, 2, "ปีฐาน").font = BOLD
    ws.cell(row["t"], 2, 0)
    ws.cell(row["revenue"], 2, "=in_revenue_base").number_format = FMT["money"]
    for i in range(1, N + 1):
        c = 2 + i
        col, prev = get_column_letter(c), get_column_letter(c - 1)
        ws.cell(3, c, f"ปี {i}").font = BOLD
        f = {
            "t": i,
            "growth": f"=in_revenue_growth_y{i}",
            "revenue": f"={prev}{row['revenue']}*(1+{col}{row['growth']})",
            "margin": f"=in_ebit_margin_y{i}",
            "ebit": f"={col}{row['revenue']}*{col}{row['margin']}",
            "nopat": f"={col}{row['ebit']}*(1-in_tax_rate)",
            "da": f"={col}{row['revenue']}*in_da_pct_revenue",
            "capex": f"={col}{row['revenue']}*in_capex_pct_revenue",
            "dnwc": f"=({col}{row['revenue']}-{prev}{row['revenue']})*in_nwc_pct_delta_revenue",
            "fcff": f"={col}{row['nopat']}+{col}{row['da']}-{col}{row['capex']}-{col}{row['dnwc']}",
            "df": f"=1/(1+x_wacc)^{col}{row['t']}",
            "pv": f"={col}{row['fcff']}*{col}{row['df']}",
        }
        for k, formula in f.items():
            cell = ws.cell(row[k], c, formula)
            cell.number_format = {"t": "0", "growth": "0.00%", "margin": "0.00%", "df": "0.0000"}.get(k, FMT["money"])
    first, last = get_column_letter(3), get_column_letter(2 + N)
    r = row["pv"] + 2
    summary = [
        ("x_pv_fcff", "PV ของ FCFF รวม", f"=SUM({first}{row['pv']}:{last}{row['pv']})", "money"),
        ("x_fcff_tv", f"FCFF ปีที่ {N + 1} = NOPAT × (1 + g) × (1 − g ÷ ROC)",
         f"={last}{row['nopat']}*(1+in_terminal_growth)*(1-in_terminal_growth/x_roc)", "money"),
        ("x_tv", "Terminal value", "=x_fcff_tv/(x_wacc-in_terminal_growth)", "money"),
        ("x_pv_tv", "PV ของ terminal value", f"=x_tv*{last}{row['df']}", "money"),
        ("x_ev", "Enterprise value", "=x_pv_fcff+x_pv_tv", "money"),
        ("x_equity", "มูลค่าส่วนของผู้ถือหุ้นบริษัทใหญ่", "=x_ev+x_bridge", "money"),
        ("x_dcf_base", "มูลค่าต่อหุ้น (DCF)", "=x_equity/in_shares", "per_share"),
        ("x_tv_share", "สัดส่วน TV ใน EV", "=x_pv_tv/x_ev", "%"),
    ]
    for nm, label, formula, unit in summary:
        ws.cell(r, 1, label).font = BOLD
        c = ws.cell(r, 2, formula)
        c.number_format = FMT[unit]
        name(wb, nm, "DCF", f"B{r}")
        if nm == "x_dcf_base":
            c.fill = KEY
        r += 1
    widths(ws, {"A": 40, **{get_column_letter(c): 16 for c in range(2, 3 + N)}})
    return row


# ---------- Sensitivity (DCF และ DDM) ----------

def grid_block(wb: Workbook, ws, top: int, title: str, x_name: str, x_label: str, y_name: str, y_label: str,
               cell_formula, prefix: str) -> int:
    """ตาราง (2·grid+1)² แถว = x (WACC/Ke), คอลัมน์ = y (g) คืนแถวถัดไป และตั้งชื่อ <prefix>_low/_high"""
    n = S["grid"]
    k = S["range_k"]
    ws.cell(top, 1, title).font = BOLD
    ws.cell(top + 1, 1, f"แถว = {x_label} · คอลัมน์ = {y_label} · กล่องสีเหลือง = ช่วงใน football field (±{k} step)")
    hr = top + 2
    ws.cell(hr, 1, f"{x_label} \\ {y_label}").font = BOLD
    for j, dj in enumerate(offsets(n)):
        c = ws.cell(hr, 2 + j, f"={y_name}+({dj})*{S['growth_step']}")
        c.number_format, c.font, c.fill = "0.00%", BOLD, HEAD
    for i, di in enumerate(offsets(n)):
        r = hr + 1 + i
        c = ws.cell(r, 1, f"={x_name}+({di})*{S['wacc_step']}")
        c.number_format, c.font, c.fill = "0.00%", BOLD, HEAD
        for j, dj in enumerate(offsets(n)):
            w = abs_ref(1, r)
            g = abs_ref(2 + j, hr)
            cell = ws.cell(r, 2 + j, cell_formula(w, g))
            cell.number_format = FMT["per_share"]
            if abs(di) <= k and abs(dj) <= k:
                cell.fill = KEY
    c0 = 2 + n - k
    r0 = hr + 1 + n - k
    box = f"Sensitivity!{abs_ref(c0, r0)}:{abs_ref(c0 + 2 * k, r0 + 2 * k)}"
    lr = hr + 2 * n + 3
    for off, (suffix, fn) in enumerate((("low", "MIN"), ("high", "MAX"))):
        ws.cell(lr + off, 1, f"{suffix} (ในกล่อง)").font = BOLD
        c = ws.cell(lr + off, 2, f"={fn}({box})")
        c.number_format = FMT["per_share"]
        name(wb, f"{prefix}_{suffix}", "Sensitivity", f"B{lr + off}")
    return lr + 3


def sheet_sensitivity(wb: Workbook, dcf_rows: dict[str, int]) -> None:
    ws = wb.create_sheet("Sensitivity")
    ws["A1"], ws["A1"].font = "Sensitivity", TITLE
    first, last = get_column_letter(3), get_column_letter(2 + N)
    fcff = f"DCF!${first}${dcf_rows['fcff']}:${last}${dcf_rows['fcff']}"
    t = f"DCF!${first}${dcf_rows['t']}:${last}${dcf_rows['t']}"
    nopat_n = f"DCF!${last}${dcf_rows['nopat']}"
    t_n = f"DCF!${last}${dcf_rows['t']}"

    def dcf_cell(w, g):
        return (f'=IF({w}>{g},(SUMPRODUCT({fcff},1/(1+{w})^{t})'
                f'+{nopat_n}*(1+{g})*(1-{g}/IF(ISNUMBER(in_terminal_roc),in_terminal_roc,{w}))/({w}-{g})/(1+{w})^{t_n}+x_bridge)/in_shares,"")')

    def ddm_cell(ke, g):
        return f'=IF({ke}>{g},in_dps_ttm*(1+{g})/({ke}-{g}),"")'

    nxt = grid_block(wb, ws, 3, "DCF: มูลค่าต่อหุ้น", "x_wacc", "WACC", "in_terminal_growth", "terminal g",
                     dcf_cell, "x_dcf")
    grid_block(wb, ws, nxt, "DDM: มูลค่าต่อหุ้น", "x_ke", "Ke", "in_ddm_growth", "g ปันผล", ddm_cell, "x_ddm")
    widths(ws, {"A": 22, **{get_column_letter(c): 13 for c in range(2, 3 + 2 * S["grid"])}})


# ---------- DDM ----------

def sheet_ddm(wb: Workbook) -> None:
    ws = wb.create_sheet("DDM")
    ws["A1"], ws["A1"].font = "Dividend Discount Model (Gordon growth)", TITLE
    header(ws, 3, ["รายการ", "ค่า", "สูตร"])
    rows = [
        ("x_d1", "DPS ปีหน้า (D₁)", "=in_dps_ttm*(1+in_ddm_growth)", "per_share", "D₀ × (1 + g)"),
        ("x_ddm_base", "มูลค่าต่อหุ้น (DDM)", '=IF(x_ke>in_ddm_growth,x_d1/(x_ke-in_ddm_growth),"Ke ≤ g")',
         "per_share", "D₁ ÷ (Ke − g)"),
    ]
    for r, (nm, label, formula, unit, note) in enumerate(rows, start=4):
        ws.cell(r, 1, label)
        c = ws.cell(r, 2, formula)
        c.number_format = FMT[unit]
        ws.cell(r, 3, note)
        name(wb, nm, "DDM", f"B{r}")
    ws.cell(5, 2).fill = KEY
    widths(ws, {"A": 30, "B": 16, "C": 30})


# ---------- Comps ----------

def sheet_comps(wb: Workbook, a: Assumptions, peers_data: dict) -> dict[str, bool]:
    """คืน {method_key: มี peer พอคำนวณไหม}"""
    ws = wb.create_sheet("Comps")
    ws["A1"], ws["A1"].font = "Comparable companies", TITLE
    ws["A2"] = "ช่องว่าง = Yahoo ไม่มีค่าหรือค่า ≤ 0 จึงไม่นับ (ดูคอลัมน์หมายเหตุ)"
    metrics = [(k, COMPS[k][0]) for k in ("comps_pe", "comps_ev_ebitda", "comps_pb")]
    header(ws, 4, ["Ticker", "ชื่อ", "Industry", "ประเทศ", "P/E", "EV/EBITDA", "P/BV", "แหล่งที่มา", "ข้อมูล ณ", "หมายเหตุ"])
    peers = [p for p in a.peers if p in peers_data]
    first = 5
    for r, sym in enumerate(peers, start=first):
        d = peers_data[sym]
        ws.cell(r, 1, sym)
        ws.cell(r, 2, d["long_name"]["value"])
        ws.cell(r, 3, d["industry"]["value"])
        ws.cell(r, 4, d["country"]["value"])
        notes = []
        for c, (_, fld) in enumerate(metrics, start=5):
            v = d[fld]["value"]
            if v is not None and v > 0:
                ws.cell(r, c, v).number_format = "0.00"
            else:
                notes.append(f"{fld}: {d[fld].get('reason') or 'ค่า ≤ 0'}")
        ws.cell(r, 8, d["trailing_pe"]["source"].split(" Ticker")[0])
        ws.cell(r, 9, d["trailing_pe"]["asof"])
        ws.cell(r, 10, "; ".join(notes) or None)
    last = max(first, first + len(peers) - 1)
    r = last + 2
    pct = V["comps_percentiles"]
    header(ws, r, ["", "", "", "", "P/E", "EV/EBITDA", "P/BV"])
    ok = {}
    for i, p in enumerate(pct):
        ws.cell(r + 1 + i, 4, f"P{p}").font = BOLD
        for c, (key, _) in enumerate(metrics, start=5):
            col = get_column_letter(c)
            rng = f"{col}{first}:{col}{last}"
            ws.cell(r + 1 + i, c, f'=IF(COUNT({rng})>=2,_xlfn.PERCENTILE.INC({rng},{p / 100}),"")').number_format = "0.00"
    to_price = {
        "comps_pe": lambda m: f"{m}*in_eps_ltm",
        "comps_ev_ebitda": lambda m: f"({m}*in_ebitda_ltm+x_bridge)/in_shares",
        "comps_pb": lambda m: f"{m}*in_equity_book/in_shares",
    }
    pr = r + len(pct) + 2
    header(ws, pr, ["", "", "", "ราคาต่อหุ้น", "P/E", "EV/EBITDA", "P/BV"])
    for i, (suffix, p) in enumerate(zip(("low", "base", "high"), pct)):
        ws.cell(pr + 1 + i, 4, f"{suffix} (P{p})").font = BOLD
        for c, (key, _) in enumerate(metrics, start=5):
            m = f"{get_column_letter(c)}{r + 1 + i}"
            cell = ws.cell(pr + 1 + i, c, f'=IF({m}="","",{to_price[key](m)})')
            cell.number_format = FMT["per_share"]
            name(wb, f"x_{key}_{suffix}", "Comps", f"{get_column_letter(c)}{pr + 1 + i}")
    for key, fld in metrics:
        ok[key] = sum(1 for s in peers if (peers_data[s][fld]["value"] or 0) > 0) >= 2
    widths(ws, {"A": 12, "B": 32, "C": 26, "D": 14, "H": 30, "I": 24, "J": 50})
    return ok


# ---------- Football field ----------

def sheet_football(wb: Workbook, a: Assumptions, results: list, comps_ok: dict[str, bool]) -> None:
    ws = wb.create_sheet("FootballField", 0)
    ws["A1"], ws["A1"].font = f"Football field · {a.ticker}", TITLE
    ws["A2"] = "แท่ง = ช่วงมูลค่าต่อหุ้นของแต่ละวิธี · แถวสุดท้าย = ราคาปัจจุบัน"
    header(ws, 4, ["วิธี", "Low", "ช่วง (High − Low)", "Base", "High", "หมายเหตุ"])
    refs = {
        "dcf_fcff": ("x_dcf_low", "x_dcf_base", "x_dcf_high"),
        "ddm": ("x_ddm_low", "x_ddm_base", "x_ddm_high"),
        "week52": ("in_week52_low", None, "in_week52_high"),
        **{k: (f"x_{k}_low", f"x_{k}_base", f"x_{k}_high") for k in COMPS},
    }
    r = 5
    for res in results:
        if res.skipped or (res.key in comps_ok and not comps_ok[res.key]):
            continue
        lo, base, hi = refs[res.key]
        ws.cell(r, 1, LABELS[res.key])
        ws.cell(r, 2, f"={lo}")
        ws.cell(r, 3, f"=E{r}-B{r}")
        ws.cell(r, 4, f"={base}" if base else None)
        ws.cell(r, 5, f"={hi}")
        r += 1
    ws.cell(r, 1, "ราคาปัจจุบัน").font = BOLD
    ws.cell(r, 2, "=in_price*0.997")
    ws.cell(r, 3, "=in_price*0.006")
    ws.cell(r, 4, "=in_price")
    ws.cell(r, 5, "=in_price*1.003")
    ws.cell(r, 6, "แท่งแคบ ๆ แทนเส้นราคา")
    for rr in range(5, r + 1):
        for c in range(2, 6):
            ws.cell(rr, c).number_format = FMT["per_share"]
    skipped = [res for res in results if res.skipped]
    for i, res in enumerate(skipped):
        ws.cell(r + 2 + i, 1, f"ไม่ได้ใช้ {LABELS[res.key]}: {res.skipped}")

    ch = BarChart()
    ch.type, ch.grouping, ch.overlap = "bar", "stacked", 100
    ch.title = f"Football field · {a.ticker} (ต่อหุ้น)"
    ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=4, max_row=r), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=5, max_row=r))
    ch.series[0].graphicalProperties.noFill = True
    ch.series[0].graphicalProperties.line.noFill = True
    ch.series[1].graphicalProperties.solidFill = "4472C4"
    price_bar = DataPoint(idx=r - 5)
    price_bar.graphicalProperties.solidFill = "C0504D"
    ch.series[1].dPt.append(price_bar)
    ch.x_axis.scaling.orientation = "maxMin"
    ch.x_axis.delete = False
    ch.y_axis.delete = False
    ch.y_axis.majorGridlines = None
    ch.legend = None
    ch.height, ch.width = 9, 16
    ws.add_chart(ch, f"A{r + 4 + len(skipped)}")
    widths(ws, {"A": 26, "B": 12, "C": 16, "D": 12, "E": 12, "F": 30})


# ---------- Sources ----------

def sheet_sources(wb: Workbook, a: Assumptions, raw: dict) -> None:
    ws = wb.create_sheet("Sources")
    ws["A1"], ws["A1"].font = "แหล่งข้อมูลทั้งหมด", TITLE
    header(ws, 3, ["แหล่งที่มา", "URL", "ข้อมูล ณ", "ดึงเมื่อ", "ใช้กับ"])
    seen: dict[tuple, list[str]] = {}
    for inp in a.inputs.values():
        k = (inp.source, inp.url, inp.asof, inp.fetched_at)
        seen.setdefault(k, []).append(inp.key)
    for sym, d in raw["peers"]["data"].items():
        if sym in a.peers:
            f = d["trailing_pe"]
            seen.setdefault((f["source"].split(" Ticker")[0] + f" (peer {sym})", f["url"], f["asof"], f["fetched_at"]),
                            []).append(f"peer {sym}")
    for r, ((src, url, asof, fetched), used) in enumerate(seen.items(), start=4):
        for c, v in enumerate((src, url, asof, fetched, ", ".join(used)), start=1):
            ws.cell(r, c, v).alignment = WRAP
    widths(ws, {"A": 70, "B": 50, "C": 24, "D": 26, "E": 40})


def build(a: Assumptions, raw: dict, out: dict, path: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    sheet_inputs(wb, a)
    sheet_historical(wb, raw)
    sheet_wacc(wb)
    dcf_rows = sheet_dcf(wb)
    sheet_sensitivity(wb, dcf_rows)
    sheet_ddm(wb)
    comps_ok = sheet_comps(wb, a, raw["peers"]["data"])
    sheet_football(wb, a, out["results"], comps_ok)
    sheet_sources(wb, a, raw)
    wb.active = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return path
