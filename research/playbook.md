# Valuation Playbook

> คู่มือเลือกวิธีและตั้งสมมติฐาน valuation สำหรับ pipeline `python -m valuation run <TICKER>`
> ทุกข้อมาจาก NotebookLM notebook "Valuation Methods" (alias `valuation-methods`) ถามเมื่อ 2026-10-31 ผ่าน agent `valuation-researcher`
> คำตอบเต็มและหลักฐานที่ยกจาก source อยู่ใน `research/nlm_log/2026-10-31_<slug>.md` (ดูท้ายไฟล์) ส่วนรายชื่อ source และ URL อยู่ใน `research/sources.md`
> สิ่งที่ notebook ไม่มี เขียนไว้ว่า **ไม่พบใน notebook** ห้ามเติมเอง

## ชื่อย่อ source ที่ใช้ในไฟล์นี้

| ชื่อย่อ | ชื่อ source เต็ม |
|---|---|
| Damodaran 2026 packet | Aswath Damodaran Updated: January 2026 - NYU Stern |
| Damodaran Ch.21 | Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern |
| Damodaran 2009 paper | Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern |
| Damodaran ERP blog | Equity Risk Premiums: Globalization and Country risk - Musings on Markets |
| Damodaran SBC blog | Stock-based Employee Compensation: Value and Pricing Effects - Musings on Markets |
| Damodaran ESOP paper | Employee Stock Options (ESOPs) and Restricted Stock: Valuation Effects and Consequences - NYU Stern |
| Damodaran Cyclicals | Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern |
| Luminor thesis | Estimating the Value of a Privately Held Bank: A Case Study of Luminor Bank AS - Digikogu |
| MDPI bank study | A Case Study of Bank Equity Valuation Methods Employed by South African, Nigerian and Kenyan Equity Researchers - MDPI |
| DiVA thesis | Valuation in High Growth Markets - DiVA-Portal |
| UNINA slides | Business Analysis and Valuation - docenti.unina.it |
| WSP SBC | Stock Based Compensation (SBC) - Wall Street Prep |
| WSP Football Field | Football Field Valuation Chart - Wall Street Prep |
| CFI EV/EBITDA | EV/EBITDA - Corporate Finance Institute |
| WallStreetMojo | Pure Play Method - WallStreetMojo |
| efinancemanagement | Unlevered Beta - efinancemanagement |
| ERM guide | How to: Excess Return Model for Valuing Financial Stocks |
| Financial Edge | REIT Valuation Methods - Financial Edge Training |
| Green Street | REIT Valuation: The NAV-based Pricing Model - Green Street |
| McKinsey Cyclicals | How to value cyclical companies - McKinsey |
| EY IFRS 16 | How the leases standard impacts company balance sheets - EY |
| ML peer paper | (Out)smart the Peer Group in Market Comparison: Building Business Valuation Multiples by Machine Learning - ResearchGate |
| NYU IPO study | Examining IPO Valuation Methods – Market Comparables and Discounted Cash Flow - NYU Stern |
| AFGR review | Valuation Multiples Through a Thematic Lens - Accounting, Finance & Governance Review |
| Lockheed thesis | Valuation of Lockheed Martin Corporation using DCF and Relative Valuation Methods - Digikogu |
| CFI Valuation Methods | Valuation Methods - Three Main Approaches to Value a Business - Corporate Finance Institute |
| CFI AFFO | Adjusted Funds From Operations (AFFO) - Corporate Finance Institute |
| Nareit | Net Asset Value - Nareit |
| IFT | Essential Concept 84: Net Asset Value Approach – REITs - IFT World |
| WSP NAV | Net Asset Value (NAV) Formula + Calculator - Wall Street Prep |
| BIWS | REIT NAV Model: Setup and How to Find the Market Value of Assets - Breaking Into Wall Street |
| A-REIT study | A-REITs Value Relevance of Performance Measures: Net Income, FFO and Fair Value of Investment Property - Western Sydney University |

---

## 1. เลือกวิธีตามประเภทธุรกิจ

| ประเภทธุรกิจ | วิธีที่ควรใช้ | วิธีที่ไม่ควรใช้ / ข้อควรระวัง | citation |
|---|---|---|---|
| บริษัทโตเต็มที่ (mature, stable) | DCF แบบ stable-growth หรือ 2-stage, DDM ถ้าปันผลใกล้ FCFE, multiples | ไม่ใช้ 3-stage model ถ้าปันผลต่ำกว่า 80% หรือเกิน 110% ของ FCFE ในช่วง 5 ปี ให้ใช้ FCFE แทน DDM | Damodaran 2026 packet |
| บริษัทโตเร็ว | DCF แบบ 3-stage หรือ n-stage | ไม่ใช้ stable-growth model และ multiple จากกำไรย้อนหลัง | Damodaran 2026 packet |
| บริษัทในตลาดเกิดใหม่ | DCF ที่ cost of equity รวม country risk premium (CRP) | ถ้าเงินเฟ้อเกิน 10% ให้ใช้ real cash flow แทน, beta ที่คำนวณกับดัชนีท้องถิ่นเชื่อถือได้น้อย | Damodaran 2026 packet, Damodaran ERP blog, DiVA thesis |
| ค้าปลีกและธุรกิจที่มีสัญญาเช่ามาก | DCF FCFF ที่นับสัญญาเช่าเป็นหนี้ (ดูข้อ 10), EV/EBITDA | ถ้านับสัญญาเช่าไม่เหมือนกันทั้งโมเดล margin, ROC และ debt ratio จะเพี้ยน | Damodaran 2026 packet |
| ธนาคารและบริษัทการเงิน | DDM, FCFE (reinvestment คือเงินกองทุนตามกฎหมายที่ต้องเพิ่ม), excess return / residual income, P/BV คู่กับ ROE | **ไม่ใช้ FCFF/WACC และ EV/EBITDA** เพราะหนี้และเงินฝากเป็นวัตถุดิบของธุรกิจ ไม่ใช่การเลือกโครงสร้างทุน และนิยาม capex กับ working capital ไม่ได้ | Damodaran 2009 paper, Damodaran Ch.21, MDPI bank study, Luminor thesis |
| REIT | NAV (NOI ÷ cap rate), P/FFO, P/AFFO, DDM, DCF บน AFFO | EPS และ P/E มักถูกมองว่าไม่สะท้อนมูลค่า แต่งานวิจัยยังเถียงกันอยู่ (ดูข้อ 7) | Financial Edge, Green Street, Nareit, A-REIT study |
| ธุรกิจ cyclical และ commodity | DCF บนกำไรหรือ margin ที่ normalize ตลอดรอบ หรือ DCF หลาย scenario ถ่วงด้วยความน่าจะเป็น, EV/EBITDA หรือ EV/Sales บนตัวเลขที่ normalize แล้ว | ไม่ใช้ปีที่กำไรสูงสุดหรือต่ำสุดเป็นปีฐาน, P/E ต่ำตอนกำไรสูงสุดไม่ได้แปลว่าถูก | Damodaran Cyclicals, McKinsey Cyclicals |
| บริษัทหลายธุรกิจ | sum-of-the-parts โดยใช้ peer ของแต่ละ segment | — | Damodaran 2009 paper, Damodaran Ch.21, MDPI bank study |

รายละเอียด: `method-by-business`, `banks-financials`, `reits`, `cyclicals-commodity`

## 2. DCF: FCFF และ FCFE

**สูตร**
- FCFF = EBIT × (1 − t) − (Capex − Depreciation) − ΔNon-cash working capital — Damodaran 2026 packet, UNINA slides
- FCFE = Net income − (Capex − Depreciation) − ΔNon-cash WC + (หนี้ใหม่ − หนี้ที่จ่ายคืน) — Damodaran 2026 packet
- FCFE เมื่อ debt ratio (DR) คงที่ = Net income − (1 − DR) × [(Capex − Depreciation) + ΔWC] — Damodaran 2026 packet

**เลือกใช้แบบไหน**
- FCFF: เมื่อคาดว่า leverage จะเปลี่ยน ข้อมูลหนี้ไม่ครบ หรือต้องการมูลค่าทั้งกิจการ — Damodaran 2026 packet
- FCFE: เมื่อ leverage คงที่ และใช้กับบริษัทการเงินทุกประเภท — Damodaran 2026 packet, Damodaran 2009 paper

**จับคู่ cash flow กับ discount rate**
- FCFF คิดลดด้วย WACC ได้ enterprise value ส่วน FCFE คิดลดด้วย cost of equity ได้ equity value — Damodaran 2026 packet
- สกุลเงินและ nominal/real ของ cash flow ต้องตรงกับ discount rate — Damodaran 2026 packet

**จาก enterprise value เป็นราคาต่อหุ้น**
1. มูลค่าสินทรัพย์ดำเนินงาน + เงินสด + เงินลงทุนในบริษัทอื่น (cross holdings) + สินทรัพย์ที่ไม่ใช่การดำเนินงาน = firm value — Damodaran 2026 packet
2. หักหนี้ (รวมหนี้สัญญาเช่า) และ minority interest ที่ปรับเป็นมูลค่าตลาดแล้ว (แปลง book เป็น market ด้วย P/B ของ sector) — Damodaran 2026 packet
3. หักมูลค่า employee options ที่ยังไม่ได้ใช้สิทธิ แล้วหารด้วยจำนวนหุ้นจริง (primary shares) โดย restricted stock นับรวมในจำนวนหุ้นแล้ว — Damodaran 2026 packet, Damodaran ESOP paper, WSP SBC
4. เงินสดให้แยกออกจาก operating cash flow แล้วบวกกลับตอนจบ — Damodaran 2026 packet

รายละเอียด: `dcf-fcff-fcfe`

## 3. Discount rate: WACC, CAPM, beta, ERP, CRP

**WACC และ cost of debt**
- WACC = ke × E/(D+E) + kd × (1 − t) × D/(D+E) โดย E และ D ใช้**มูลค่าตลาด** ไม่ใช่มูลค่าทางบัญชี — Damodaran 2026 packet
- cost of debt = Rf + default spread (จาก YTM หรือ synthetic rating) ไม่ใช่อัตราดอกเบี้ยหน้าตั๋วหรือดอกเบี้ยจ่ายหารหนี้ตามบัญชี — Damodaran 2026 packet

**CAPM และ risk-free rate**
- ke = Rf + β × ERP — Damodaran 2026 packet
- Rf ต้องไม่มี default risk และเป็นสกุลเงินเดียวกับ cash flow ถ้าพันธบัตรรัฐบาลของตลาดเกิดใหม่มี default risk ให้หัก country default spread ออกก่อน (ใช้ spread จาก sovereign bond, CDS หรือ rating) — Damodaran 2026 packet

**Beta**
- regression beta มี standard error สูง และสะท้อนธุรกิจกับ leverage ในอดีต ส่วน bottom-up (pure-play) beta มี noise น้อยกว่า: หา peer → unlever → เฉลี่ย → relever ด้วย D/E ของบริษัทเป้าหมาย — Damodaran 2026 packet, WallStreetMojo, efinancemanagement
- unlever: βU = βL ÷ [1 + (1 − t) × D/E] · relever: βL = βU × [1 + (1 − t) × D/E] (D/E ใช้มูลค่าตลาด) — Damodaran 2026 packet, efinancemanagement, Luminor thesis
- ปรับเรื่องเงินสด: β operating = βU ÷ (1 − Cash/Firm value) เพราะ beta ของเงินสดเท่ากับ 0 — Damodaran 2026 packet

**Equity risk premium (ERP)**
- historical ERP ขึ้นกับช่วงเวลาและวิธีเฉลี่ยมาก standard error เกิน 2% แม้ใช้ข้อมูล 90 ปี ส่วน implied ERP มองไปข้างหน้าและสัมพันธ์กับผลตอบแทนในอนาคตได้ดีกว่า — Damodaran 2026 packet

**Country risk premium (CRP)**
- วิธีประมาณ: default spread ของประเทศ, relative equity volatility หรือ default spread × (σ ตลาดหุ้น ÷ σ พันธบัตรรัฐบาล) — Damodaran 2026 packet, Damodaran ERP blog, DiVA thesis
- ใส่เข้า ke ได้ 3 แบบ: Rf + β×ERP + CRP · Rf + β×(ERP + CRP) · Rf + β×ERP + λ×CRP (λ ตามสัดส่วนรายได้ในประเทศ) บริษัทที่มีรายได้หลายประเทศควรใช้ CRP ถ่วงด้วยรายได้หรือ λ — Damodaran 2026 packet, DiVA thesis
- **ไม่พบใน notebook:** ค่า Rf, ERP และ CRP ของไทย ให้ดึงจาก ThaiBMA และ Damodaran Online ตาม Trust sources ใน `spec.md`

รายละเอียด: `wacc-capm`, `beta`, `erp-crp`

## 4. Terminal value

- Gordon growth: TV(n) = CF(n+1) ÷ (r − g) โดย r เป็น WACC สำหรับ FCFF และ cost of equity สำหรับ FCFE หรือปันผล — Damodaran 2026 packet
- exit multiple เป็นการตั้งราคา (pricing) ไม่ใช่ intrinsic value source ระบุว่า "Never appropriate in an intrinsic valuation" ถ้าจะใช้ ให้แสดงเป็นแท่งแยกใน football field — Damodaran 2026 packet
- **เพดานของ g:** ต้องไม่เกินอัตราโตของเศรษฐกิจ (ต่ำกว่าหรือติดลบได้) และ Rf เป็นเพดานโดยปริยาย เพราะ Rf = เงินเฟ้อ + real rate เทียบได้กับ nominal GDP growth = เงินเฟ้อ + real growth ถ้า cash flow เป็น nominal ต้องใช้ g แบบ nominal ในสกุลเงินเดียวกัน — Damodaran 2026 packet
- **ความสอดคล้องกับ reinvestment:** ใน stable growth reinvestment rate = g ÷ ROC และ payout = 1 − g ÷ ROE ดังนั้น FCFF(n+1) = EBIT(n+1) × (1 − t) × (1 − g/ROC) — Damodaran 2026 packet
- ช่วง terminal ให้ beta เข้าใกล้ 1, debt ratio เข้าใกล้ค่าเฉลี่ยอุตสาหกรรม และ excess return ลดลงเข้าหา 0 — Damodaran 2026 packet
- สัดส่วน TV ต่อมูลค่ารวมและความยาวของช่วง forecast **ไม่พบกฎใน notebook** มีแค่ตัวอย่าง: Heineken ใช้ forecast 10 ปี TV ประมาณ 70% (Damodaran 2026 packet) และ Luminor ใช้ 5 ปี TV 46% (Luminor thesis) ส่วนสิ่งที่ทำให้ช่วงโตเร็วยาวขึ้นคือขนาดบริษัทเทียบตลาด ความแข็งแรงของความได้เปรียบทางการแข่งขัน และกฎระเบียบ — Damodaran 2026 packet, Damodaran Ch.21

รายละเอียด: `terminal-value`

## 5. Dividend discount model (DDM)

- stable: P0 = D1 ÷ (ke − g) ใช้ได้เมื่อ ke > g — MDPI bank study, Damodaran 2009 paper
- 2-stage: PV ของ DPS ช่วงโตเร็ว n ปี + PV ของราคาปลายงวด = DPS(n+1) ÷ (ke stable − g) — Damodaran 2009 paper, Damodaran Ch.21
- g = retention ratio × ROE และ payout ใน stable growth = 1 − g/ROE — Damodaran 2009 paper, Damodaran Ch.21
- เหมาะกับธนาคาร ประกัน และ utility ที่โตช้า แต่ถ้าธนาคารจ่ายปันผลต่ำกว่าที่จ่ายได้ การใช้ปันผลปัจจุบันจะทำให้มูลค่าต่ำเกินจริง — Damodaran 2026 packet, Damodaran 2009 paper

รายละเอียด: `ddm`

## 6. Excess return model และธนาคาร

- Equity value = Book equity₀ + Σ PV[(ROE_t − ke) × Book equity_(t−1)] + PV ของ terminal value โดย terminal value = (ROE terminal − ke) × Book equity_n ÷ (ke − g) — MDPI bank study, Luminor thesis, ERM guide, Damodaran 2009 paper
- justified P/BV = (ROE − g) ÷ (ke − g) — MDPI bank study, Damodaran 2009 paper
- FCFE ของธนาคาร = กำไรสุทธิ − เงินกองทุนตามกฎหมายที่ต้องเพิ่ม — Damodaran 2009 paper, Damodaran Ch.21
- ในงานสำรวจนักวิเคราะห์ธนาคารแอฟริกาใต้ ไนจีเรีย และเคนยา วิธีที่ใช้มากที่สุดคือหา P/BV หรือ P/tNAV ที่สมควรจาก ROE/ROTE ที่ยั่งยืน และนักวิเคราะห์มากกว่า 90% ใช้ multiples ด้วย (ตัวเลขนี้มาจากตลาดเหล่านั้นเท่านั้น) — MDPI bank study

รายละเอียด: `banks-financials`

## 7. REIT

**FFO และ AFFO**
- FFO = กำไรสุทธิ + ค่าเสื่อมราคาและค่าตัดจำหน่ายอสังหาริมทรัพย์ ไม่รวมกำไรหรือขาดทุนจากการขายอสังหาริมทรัพย์ (นิยามมาจาก white paper ของ NAREIT ปี 1991 และแนวทางปี 2018 ให้บวกกลับเฉพาะค่าเสื่อมของอสังหาริมทรัพย์เพื่อการลงทุน) — Financial Edge, A-REIT study
- AFFO = FFO − capex ที่เกิดประจำ − tenant improvements − ค่า leasing commissions และปรับ straight-line rent ออก — Financial Edge, Green Street, CFI AFFO
- AFFO ไม่มีนิยามทางการจาก NAREIT จึงเทียบข้าม REIT ได้ยาก ต้องดูว่าแต่ละบริษัทคำนวณอย่างไร — CFI AFFO

**NAV**
1. ประเมินมูลค่าตลาดของอสังหาริมทรัพย์: NOI ล่วงหน้า ÷ cap rate (BIWS แนะนำให้ใช้ cap rate รายภูมิภาค แทนการเอา NOI 3 เดือนมาคูณ 4 แล้วใช้ cap rate เดียวทั้งพอร์ต) — Nareit, BIWS, Green Street
2. บวกสินทรัพย์อื่นและรายได้ข้างเคียง (ค่าบริหาร, JV) หักค่าใช้จ่ายส่วนกลางและ capex ในอนาคตที่คาดไว้ ให้ goodwill และ intangibles เป็น 0 — WSP NAV, BIWS
3. หักหนี้และหนี้สินทั้งหมด: Green Street ปรับหนี้เป็นมูลค่าตลาด ส่วน Financial Edge และ IFT ใช้มูลค่าทางบัญชี เว้นแต่มีข้อมูลตลาดที่ดีกว่า — Green Street, Financial Edge, IFT
4. หารด้วยจำนวนหุ้น diluted — Green Street, Nareit
- cap rate เป็นตัวแปรที่สำคัญที่สุด และควรเทียบ cap rate หลังหักเงินสำรอง capex — Green Street
- ราคาอาจต่ำกว่า NAV (ถูกเกินไป) หรือสูงกว่า NAV เพราะคุณภาพสินทรัพย์ ผู้บริหาร หรือการเติบโต ส่วน Green Street ผูก premium กับ franchise value, ความเสี่ยงงบดุล, governance และค่าใช้จ่ายส่วนกลาง — Nareit, IFT, Green Street

**ทำไม EPS อาจไม่สะท้อนมูลค่า และหลักฐานที่ยังเถียงกันอยู่**
- NAREIT เห็นว่าค่าเสื่อมราคาสมมติว่าอสังหาริมทรัพย์เสื่อมมูลค่าตามเวลา แต่มูลค่าจริงขึ้นลงตามตลาด และภายใต้ IAS 40 ส่วนเปลี่ยนแปลง fair value ก็ไหลผ่านงบกำไรขาดทุน FFO ตัดสองส่วนนี้ออก — A-REIT study
- งานวิจัยยังไม่มีข้อสรุป: ใน A-REIT ปี 2012–2021 มีแต่กำไรสุทธิที่อธิบายราคาได้อย่างมีนัยสำคัญ บางงานในอดีตได้ผลแบบเดียวกัน แต่อีกหลายงานพบว่า FFO อธิบายได้ดีกว่า — A-REIT study
- REIT ต้องจ่ายปันผลอย่างน้อย 90% ของกำไรที่ต้องเสียภาษี จึงใช้ DDM และ AFFO payout ประกอบได้ (source ไม่ได้ระบุว่าเป็นกฎของประเทศไหน) — Financial Edge
- **ไม่พบใน notebook:** ช่วง P/FFO, P/AFFO, cap rate หรือส่วนลดจาก NAV ที่สมเหตุสมผล และกฎของ REIT หรือกองทุนอสังหาริมทรัพย์ไทย

รายละเอียด: `reits`, `reits-v2`

## 8. ธุรกิจ cyclical และ commodity

- ปีฐานที่กำไรสูงสุดทำให้มูลค่าสูงเกินจริง ปีที่ต่ำสุดทำให้ต่ำเกินจริง ให้ normalize ด้วยกำไรเฉลี่ย 5–10 ปี หรือ margin/ROC เฉลี่ยตลอดรอบคูณรายได้หรือเงินทุนปัจจุบัน หรือ margin เฉลี่ยของ sector ถ้าประวัติสั้น — Damodaran Cyclicals
- ต้อง normalize ทุกตัวไปพร้อมกัน (ROC, reinvestment, ต้นทุนการเงิน, debt ratio) และห้ามใส่ high growth ซ้อนบนฐานที่ normalize แล้ว — Damodaran Cyclicals
- ราคา commodity: ใช้ค่าเฉลี่ยในอดีตที่ปรับเงินเฟ้อ, ต้นทุนส่วนเพิ่ม (supply-demand) หรือ futures curve หรือใช้ scenario และ Monte Carlo — Damodaran Cyclicals
- P/E ต่ำสุดตอนกำไรสูงสุดและสูงสุดตอนกำไรต่ำสุด, EV/EBITDA ดูนิ่งกว่าแต่ source เตือนว่าเป็นความนิ่งที่หลอกตา ให้ใช้ multiple กับกำไรที่ normalize แล้ว และกำไรที่เสี่ยงกว่าควรได้ multiple ต่ำกว่า — Damodaran Cyclicals
- ช่วงที่ใช้เฉลี่ยต้องยาวพอให้ครอบคลุมทั้งรอบ ซึ่งอาจสั้นแค่ 2–3 ปีหรือยาวเกิน 10 ปี — Damodaran Cyclicals

**วิธีของ McKinsey: DCF หลาย scenario ถ่วงด้วยความน่าจะเป็น**
1. scenario "รอบปกติ" ที่ตั้ง continuing value ไว้ที่ระดับ normalize บนเส้นแนวโน้มระยะยาว — McKinsey Cyclicals
2. scenario "แนวโน้มใหม่" ที่สร้างจากผลงานช่วงหลัง — McKinsey Cyclicals
3. ทุก scenario ต้องมีเหตุผลทางเศรษฐกิจรองรับ แล้วถ่วงด้วยความน่าจะเป็น (ตัวอย่าง 50/50 ใน source เป็นแค่การสาธิต) — McKinsey Cyclicals
- ธุรกิจที่ผูกกับราคา commodity ให้ทำโมเดลแยกปริมาณกับส่วนต่างราคา แทนการพยากรณ์รายได้รวม — McKinsey Cyclicals
- McKinsey พบว่าราคาหุ้นผันผวนกว่ามูลค่า DCF ที่รู้อนาคตล่วงหน้า ตีความว่าตลาดยึดติดกับกำไรปัจจุบัน และ consensus forecast พยากรณ์รอบไม่ได้ — McKinsey Cyclicals
- ทั้งสอง source ตั้ง terminal value ที่ระดับ normalize เหมือนกัน แต่ Damodaran เน้น normalize ส่วน McKinsey เน้นถ่วงหลาย scenario (การเอามาเทียบกันเป็นการเรียบเรียงของ notebook เอง ทั้งสองบทความไม่ได้อ้างถึงกัน) — Damodaran Cyclicals, McKinsey Cyclicals
- **ไม่พบใน notebook:** margin กลางรอบ, วิธีตั้งน้ำหนัก scenario ที่เป็นตัวเลข

รายละเอียด: `cyclicals-commodity`, `cyclicals-commodity-v2`

## 9. Relative valuation (multiples)

**สูตรและตัวขับเคลื่อน**
- P/E = ราคา ÷ EPS ตัวขับคือ growth, payout, ROE (บวก) และ cost of equity (ลบ) ใช้กับบริษัทขาดทุนไม่ได้ — MDPI bank study
- EV/EBITDA = (market cap + หนี้ − เงินสด) ÷ EBITDA ตัวขับคือ growth (บวก) และ cost of capital, reinvestment, ภาษี (ลบ) — CFI EV/EBITDA, Damodaran 2026 packet
- P/BV = ราคา ÷ book value ต่อหุ้น justified = (ROE − g) ÷ (ke − g) ตัวขับหลักคือ ROE เหมาะกับธนาคาร — MDPI bank study, Damodaran 2009 paper
- EV/EBITDA และ EV/Sales เหมาะกับธุรกิจ cyclical แต่ไม่ใช้กับธนาคารและประกัน — Damodaran Cyclicals, Damodaran 2009 paper
- EV/EBITDA มีข้อเสีย: ไม่สนใจ capex ใช้แทนกระแสเงินสดไม่ได้ และปรับเรื่อง growth ได้ยาก — CFI EV/EBITDA
- EV/Revenue ใช้ได้เมื่อบริษัทยังขาดทุน — NYU IPO study
- ถ้า leverage ของ peer ต่างกันมาก ให้ใช้ enterprise multiple — Lockheed thesis
- PEG: **ไม่พบใน notebook** สูตรที่ notebook ตอบมาในรอบแรกไม่มี source รองรับ

**Trailing หรือ forward**
- forward P/E ใช้ประมาณการ 1–3 ปีข้างหน้า และช่วยได้เมื่อกำไรย้อนหลังผิดปกติ (ตัวอย่างใน source: trailing P/E 296 เทียบกับ forward 55 ของหุ้นตัวเดียวกัน) — MDPI bank study, UNINA slides
- หลักฐานว่าแบบไหนแม่นกว่ายังขัดกัน: งาน M&A มักใช้ trailing ส่วนนักวิเคราะห์ใช้ P/E มากที่สุดใน 20 จาก 25 อุตสาหกรรม — AFGR review, NYU IPO study

**กฎความสอดคล้อง**
- equity multiple ต้องใช้ตัวหารฝั่ง equity (EPS, book equity) ส่วน enterprise multiple ใช้ตัวหารฝั่งกิจการ (EBITDA, EBIT, sales) — UNINA slides

**เลือก peer**
- เกณฑ์: อุตสาหกรรม ขนาด ตำแหน่งในการแข่งขัน growth และกำไร leverage และความเสี่ยง และต้องจดทะเบียนในตลาด — UNINA slides, Luminor thesis
- ใช้รหัสอุตสาหกรรมกว้าง ๆ อย่างเดียวไม่พอ: GICS ดีกว่า SIC และ NAICS และการแบ่งกลุ่มให้ละเอียดขึ้นทำให้ error ลดลง แต่ยิ่งเพิ่มเกณฑ์ กลุ่ม peer ก็ยิ่งเล็กลงเร็ว — AFGR review, NYU IPO study, ML peer paper
- การเลือก peer ด้วยมือเสี่ยงต่อ bias (เลือกเฉพาะตัวที่ได้ผลตามที่อยากได้) — ML peer paper
- ปรับความต่างของ peer: หาร multiple ด้วยตัวขับ (เช่น P/BV ÷ ROE) ซึ่งสมมติว่าสัมพันธ์เชิงเส้น หรือ regress multiple กับตัวขับ (เช่น P/E กับ growth, beta, payout) แล้วแทนค่าของบริษัทเป้าหมาย — Damodaran Cyclicals, Damodaran Ch.21, Damodaran 2009 paper
- **ค่าเฉลี่ยหรือมัธยฐาน:** นักปฏิบัติมักใช้มัธยฐาน นักวิชาการบางส่วนใช้ harmonic mean ในงานวิจัย มัธยฐานให้ median error ต่ำสุด harmonic mean ให้ mean error ต่ำสุด สรุปว่าไม่มีวิธีที่ดีที่สุดวิธีเดียว — ML peer paper
- ถ้า multiple ของ peer กระจุกตัวใช้ค่าเฉลี่ยหรือมัธยฐานก็ได้ ถ้ากระจายกว้างให้ใช้มัธยฐาน และตัด peer ที่ตัวเลขผิดปกติออกก่อน — Lockheed thesis
- จำนวน peer: **ไม่พบกฎใน notebook** มีแค่ตัวอย่าง 5–10 ตัว (CFI), 11 ตัว (Luminor), 6 ตัว (Lockheed) — CFI EV/EBITDA, Luminor thesis, Lockheed thesis

**ความแม่นของ multiples**
- ใช้ค่าเฉลี่ยของอุตสาหกรรม: median absolute error ประมาณ 25% สำหรับ EV/EBITDA, EV/EBIT และ P/E แต่ 47% สำหรับ EV/Sales — ML peer paper
- ในงานศึกษา IPO ของ NYU พบว่า P/E และ EV/Revenue แม่นที่สุด ส่วน EV/EBITDA และ EV/EBIT คลาดเคลื่อนมาก (กลุ่มตัวอย่างเล็ก) — NYU IPO study

รายละเอียด: `multiples-pe-ev-pbv`, `multiples-pe-ev-pbv-v2`, `peer-selection`, `peer-selection-v2`

## 10. รายการที่ต้องปรับ: สัญญาเช่าและ stock-based compensation

**สัญญาเช่า (สำคัญกับค้าปลีกอย่าง CPALL)**
- หนี้สัญญาเช่า = PV ของภาระค่าเช่าคิดลดด้วย pre-tax cost of debt และตั้งสินทรัพย์ที่เช่าเท่ากัน — Damodaran 2026 packet
- EBIT ที่ปรับแล้ว = EBIT ในงบ + ค่าเช่าปีปัจจุบัน − ค่าเสื่อมราคาของสินทรัพย์ที่เช่า แล้วใส่หนี้สัญญาเช่าในน้ำหนัก WACC และหักใน bridge จาก EV เป็น equity — Damodaran 2026 packet
- IFRS และ US GAAP ให้บันทึกสัญญาเช่าในงบดุลตั้งแต่ปี 2019 — Damodaran 2026 packet
- ตัวอย่าง The Gap ของ Damodaran ใช้งบปี 2003 ซึ่งเป็นยุคก่อน IFRS 16 — Damodaran 2026 packet

**ผลของ IFRS 16 ต่องบการเงิน**
- IFRS 16 ใช้กับรอบบัญชีที่เริ่มตั้งแต่ 1 ม.ค. 2019 ยกเว้นสัญญาเช่าไม่เกิน 12 เดือนที่ไม่มีสิทธิซื้อ และสินทรัพย์มูลค่าต่ำ — EY IFRS 16
- ในบริษัท Fortune Global 500 จำนวน 58 แห่ง กลุ่มค้าปลีกและเครื่องแต่งกาย สายการบิน และขนส่ง มีสินทรัพย์รวมเพิ่มเฉลี่ยประมาณ 14% และหนี้สินเพิ่มเกิน 20% — EY IFRS 16
- EBITDA มักสูงขึ้น เพราะค่าเช่าเปลี่ยนเป็นค่าเสื่อมราคากับดอกเบี้ย และ net debt ในงบดุลรวมหนี้สัญญาเช่าแล้ว จึงไม่ต้องคำนวณ "adjusted net debt" (net debt + ค่าเช่า × ตัวคูณ) แยกเหมือนก่อน — EY IFRS 16
- ค่าเช่าย้ายจากกระแสเงินสดดำเนินงานไปเป็นกระแสเงินสดจัดหาเงิน บางบริษัทรายงาน "free cash flow after leases" แยก — EY IFRS 16
- บริษัทส่วนใหญ่ไม่ปรับตัวเลขปีก่อนย้อนหลัง แต่แสดงคอลัมน์ "รวม" และ "ไม่รวม" IFRS 16 คู่กัน ต้องระวังเมื่อเทียบตัวเลขข้ามปี — EY IFRS 16
- **การจับคู่ EV กับ EBITDA หลัง IFRS 16: ไม่พบกฎใน notebook** EY แสดงแค่ว่า net debt รวมหนี้สัญญาเช่า และ EBITDA ไม่รวมค่าเช่า แต่ไม่ได้บอกว่าต้องจับคู่กัน ถ้าจะใช้กฎ "EV รวมหนี้สัญญาเช่าคู่กับ EBITDA หลัง IFRS 16" ต้องเขียนว่าเป็นข้อสรุปของผู้เรียนเอง — EY IFRS 16
- **ไม่พบใน notebook:** TFRS 16 และค้าปลีกไทย, ค่าเช่าที่ผันแปรตามยอดขาย

**Stock-based compensation (SBC)**
- ห้ามบวก SBC กลับเป็น non-cash เพราะเป็นค่าใช้จ่ายที่จ่ายเป็นหุ้นแทนเงินสด ถ้าบวกกลับจะได้มูลค่าสูงเกินจริง — Damodaran 2026 packet, Damodaran SBC blog, WSP SBC
- options ที่ออกไปแล้วให้ตีมูลค่าด้วย option pricing แล้วหักจาก equity value ก่อนหารด้วยหุ้นจริง วิธี fully diluted ให้ราคาต่ำเกินไป ส่วน treasury stock method ให้ราคาสูงเกินไป — Damodaran ESOP paper, Damodaran 2026 packet

รายละเอียด: `dcf-mistakes`, `sbc-dilution`, `leases-ifrs16`

## 11. ช่วงสมมติฐานที่ notebook ให้ไว้

> ตัวเลขข้างล่างเป็น**ตัวอย่างหรือตารางใน source** ไม่ใช่ค่าแนะนำ ค่าจริงที่ใส่ในโมเดลต้องดึงจาก Trust sources ใน `spec.md` พร้อมวันที่

| สมมติฐาน | สิ่งที่ notebook บอก | citation |
|---|---|---|
| Terminal growth (g) | ไม่เกินอัตราโตของเศรษฐกิจ และไม่ควรเกิน Rf ตัวอย่าง ERM ใช้ 3% ตาม GDP growth ของประเทศ | Damodaran 2026 packet, ERM guide |
| Rf สหรัฐ 10 ปี | ตัวอย่างในอดีต 0.78% ถึงประมาณ 4% ต้นปี 2026 | Damodaran 2026 packet, ERM guide |
| ERP สหรัฐ (implied) | 6.17% (มิ.ย. 2012), 5.20% (ม.ค. 2020), 4.24% (ธ.ค. 2021), ประมาณ 4.2–4.5% (ต้นปี 2025–2026) | Damodaran 2026 packet, Damodaran ERP blog |
| ERP ที่ Damodaran ใช้เอง | 5.5% ก่อนปี 1998, 4% ปี 1998 ถึง ก.ย. 2008, 5–6% หลังวิกฤตปี 2008 | Damodaran ERP blog |
| ERP รวม CRP รายภูมิภาค (ม.ค. 2026) | อเมริกาเหนือ 4.45%, ยุโรปตะวันตก 5.27%, เอเชีย 5.72%, ละตินอเมริกา 8.46% | Damodaran 2026 packet |
| Country default spread | AAA 0–0.23%, investment grade 1.10–3.24%, กลุ่มวิกฤต 8.41–26.66% | Damodaran 2026 packet |
| สัดส่วน σ หุ้น ÷ σ พันธบัตร | ประมาณ 1.5 | Damodaran 2026 packet, Damodaran ERP blog |
| ความยาว forecast | ไม่มีกฎ ตัวอย่าง 10 ปี (Heineken) และ 5 ปี (Luminor) | Damodaran 2026 packet, Luminor thesis |
| Beta ช่วง terminal | เข้าใกล้ 1 | Damodaran 2026 packet |
| ช่วง normalize กำไร cyclical | มักเฉลี่ย 5–10 ปี แต่ต้องยาวพอให้ครอบคลุมทั้งรอบ (2–3 ปีถึงเกิน 10 ปี) | Damodaran Cyclicals |
| จำนวน peer | ไม่มีกฎ ตัวอย่าง 5–10, 6 และ 11 ตัว | CFI EV/EBITDA, Lockheed thesis, Luminor thesis |
| error ของ multiples จากค่าเฉลี่ยอุตสาหกรรม | ประมาณ 25% (EV/EBITDA, EV/EBIT, P/E) และ 47% (EV/Sales) | ML peer paper |
| **ไม่พบใน notebook** | Rf, ERP และ CRP ของไทย, beta รายอุตสาหกรรม, ช่วง WACC ที่แนะนำ, cap rate และ P/FFO ที่สมเหตุสมผล | — |

## 12. ข้อผิดพลาดที่พบบ่อย

1. จับคู่ cash flow กับ discount rate ผิด เช่น FCFE คิดลดด้วย WACC ทำให้ equity สูงเกินจริง หรือ FCFF คิดลดด้วย cost of equity — Damodaran 2026 packet
2. สกุลเงินหรือ nominal/real ของ cash flow, Rf และ g ไม่ตรงกัน — Damodaran 2026 packet
3. ตั้ง g ใน terminal สูงกว่าเศรษฐกิจ หรือไม่สอดคล้องกับ Rf — Damodaran 2026 packet
4. reinvestment ไม่สอดคล้องกับ growth เช่น สมมติว่า capex เท่ากับค่าเสื่อมแต่ยังโตต่อ ใน terminal ต้องให้ reinvestment = g ÷ ROC — Damodaran 2026 packet, Damodaran Ch.21
5. นับซ้ำ: บวกมูลค่าสินทรัพย์ที่สร้าง cash flow อยู่แล้วเข้าไปอีก หรือบวกเงินสดทั้งที่ดอกเบี้ยรับอยู่ใน cash flow แล้ว — Damodaran 2026 packet
6. บวก SBC กลับเป็น non-cash — Damodaran 2026 packet, Damodaran SBC blog, WSP SBC
7. นับสัญญาเช่าไม่เหมือนกันทั้งโมเดล — Damodaran 2026 packet
8. ใช้ปีที่กำไรสูงสุดหรือต่ำสุดของรอบเป็นปีฐาน — Damodaran Cyclicals
9. ใช้ FCFF หรือ EV/EBITDA กับธนาคาร — Damodaran 2009 paper
10. relative valuation: สมมติว่าตลาดตั้งราคาถูกโดยเฉลี่ย (ทั้ง sector อาจแพงหรือถูกเกินจริงพร้อมกัน), สมมติว่า peer มีความเสี่ยงและ growth เท่ากัน, ผสม equity multiple กับ enterprise multiple — UNINA slides, ERM guide, Damodaran 2009 paper
11. เลือก peer จากรหัสอุตสาหกรรมกว้าง ๆ อย่างเดียว, เลือกเฉพาะ peer ที่ได้ผลตามที่อยากได้, ไม่ตัดตัวที่ผิดปกติออก — ML peer paper, Lockheed thesis
12. เทียบตัวเลขก่อนและหลัง IFRS 16 ปนกัน เพราะหลายบริษัทไม่ปรับตัวเลขปีก่อนย้อนหลัง — EY IFRS 16

รายละเอียด: `dcf-mistakes`, `peer-selection`, `peer-selection-v2`, `leases-ifrs16`

## 13. สร้าง football field

> รอบ v2 ตรวจเทียบกับข้อความใน source แล้วพบว่า log รอบแรกเขียนเกินหลักฐานบางข้อ (กฎ percentile 25/75 และการตั้งปลายแท่ง DCF) ข้อเหล่านั้นจึงย้ายไปอยู่ใน "ไม่พบใน notebook" ด้านล่าง

1. **คืออะไร:** กราฟแท่งลอยแนวนอนที่วางช่วงมูลค่าจากหลายวิธีไว้คู่กัน ใช้ตรวจว่าแต่ละวิธีให้ผลใกล้กันหรือไม่ — WSP Football Field
2. **แท่งที่ใส่:** ช่วงราคา 52 สัปดาห์, analyst target price, comparable companies, precedent transactions และ DCF (LBO, sum-of-the-parts และ liquidation ใส่ได้ถ้ามี) และใส่เส้นค่าเฉลี่ยของทุกวิธีได้ — CFI Valuation Methods, WSP Football Field
3. **ช่วงของแท่ง DCF:** source ไม่ได้บอกตรง ๆ ว่าปลายแท่งตั้งอย่างไร แต่งานที่ใช้ DCF ทำตาราง sensitivity ระหว่าง WACC กับ long-term growth หรือ discount rate กับ terminal multiple และใน NYU IPO study ขอบล่างของช่วง DCF แม่นที่สุด — Lockheed thesis, NYU IPO study
4. **รวมหลายวิธี:** ทำ DCF ก่อนแล้วใช้ relative valuation ตรวจซ้ำ การเฉลี่ย multiple ที่ดีที่สุดกับ DCF ช่วยลดการตั้งราคาผิดของบริษัทที่ตั้งราคาผิดมากที่สุด และให้ได้ช่วงจากหลายวิธีก่อนแล้วจึงใช้วิจารณญาณ — Lockheed thesis, NYU IPO study
5. **อ่านผลกับราคาปัจจุบัน:** มีแค่ตัวอย่าง Lockheed ที่ถ้า DCF สูงกว่าราคาตลาดอ่านว่าถูก และถ้า DCF กรณีต่ำให้ค่าต่ำกว่าราคาอ่านว่าแพงเล็กน้อย ไม่มี source เรื่อง football field ที่บอกวิธีอ่านเส้นราคาตรง ๆ — Lockheed thesis
6. **ใน Excel:** notebook ตอบในรอบแรกว่าใช้ stacked bar แนวนอนที่มีคอลัมน์ Low, High, Base (= Low) และ Spread (= High − Low) ตั้ง series Base เป็น no fill แล้วเพิ่มเส้นราคาด้วย scatter series (อ้าง WSP Football Field แต่รอบ v2 ไม่ได้ตรวจซ้ำ ถือว่าหลักฐานอ่อน) — WSP Football Field

**ไม่พบใน notebook:** กฎตั้งปลายแท่ง (percentile หรือ min/max), น้ำหนักระหว่าง DCF, comps และ precedents

รายละเอียด: `football-field`, `football-field-v2`

---

## 14. สิ่งที่ไม่พบใน notebook (ต้องหาจาก Trust sources อื่นหรือถามผู้เรียน)

- Rf, ERP และ CRP ของไทย → ThaiBMA และ Damodaran Online ตาม `spec.md`
- beta รายอุตสาหกรรม, Blume adjustment
- ช่วง WACC หรือ cost of equity ที่แนะนำ
- กฎสัดส่วน terminal value ต่อมูลค่ารวม และกฎความยาว forecast
- จำนวน peer ขั้นต่ำ และกฎตัดตัวผิดปกติที่เป็นตัวเลข
- PEG
- กฎจับคู่ EV กับ EBITDA หลัง IFRS 16 (EBITDAR) และ TFRS 16 ของไทย
- ช่วง P/FFO, P/AFFO, cap rate และกฎของ REIT ไทย
- กฎตั้งปลายแท่งและน้ำหนักของแต่ละวิธีใน football field

## 15. ไฟล์ log ที่อ้างถึง

ทุกไฟล์อยู่ใน `research/nlm_log/` และขึ้นต้นด้วย `2026-10-31_`

| slug | หัวข้อ |
|---|---|
| `dcf-fcff-fcfe` | FCFF/FCFE, จับคู่ discount rate, จาก EV เป็นราคาต่อหุ้น |
| `wacc-capm` | WACC, cost of debt, CAPM, Rf |
| `beta` | regression vs bottom-up beta, unlever/relever, ปรับเรื่องเงินสด |
| `erp-crp` | ERP, CRP, ตาราง ม.ค. 2026 |
| `terminal-value` | Gordon vs exit multiple, เพดาน g, reinvestment |
| `ddm` | DDM แบบ stable และ 2-stage |
| `dcf-mistakes` | ข้อผิดพลาด DCF และการนับสัญญาเช่า |
| `sbc-dilution` | SBC, options, dilution |
| `multiples-pe-ev-pbv` | P/E, EV/EBITDA, P/BV, กฎความสอดคล้อง |
| `peer-selection` | เลือก peer และปรับความต่าง |
| `football-field` | สร้างและอ่าน football field |
| `banks-financials` | ธนาคาร, excess return model |
| `reits` | FFO, AFFO, NAV |
| `cyclicals-commodity` | normalize กำไร, ราคา commodity |
| `method-by-business` | วิธีตามประเภทธุรกิจ, สัญญาเช่า |
| `multiples-pe-ev-pbv-v2` | trailing vs forward, ข้อเสีย EV/EBITDA (source รอบ deep เสริม) |
| `peer-selection-v2` | mean vs median, GICS, ความแม่นของ multiples |
| `football-field-v2` | แท่ง analyst target, รวมหลายวิธี, ตรวจหลักฐาน log รอบแรก |
| `reits-v2` | NAV หลาย source, หลักฐาน NI vs FFO |
| `cyclicals-commodity-v2` | วิธีหลาย scenario ของ McKinsey |
| `leases-ifrs16` | ผลของ IFRS 16 ต่องบ, EBITDA, net debt |
