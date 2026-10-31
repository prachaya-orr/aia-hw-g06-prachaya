# Terminal value: Gordon growth vs exit multiple, cap ของ g, ความสัมพันธ์ g–reinvestment–ROIC, สัดส่วนมูลค่า, ความยาว forecast

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 1f3d0023-f37a-4395-86a1-3658178c5ea0 (คำถามหลัก), 7e014b52-c42d-4e5c-85e9-bb601361fc01 (follow-up)

## คำถาม

1. "Explain terminal value in a DCF: the Gordon growth (perpetuity growth) formula versus the exit multiple approach. What cap should the stable growth rate have relative to the risk-free rate or nominal economic growth? How are growth, reinvestment rate and return on capital (ROIC) linked in stable growth? What share of total value does terminal value typically represent, and how long should the explicit forecast period be?"
2. Follow-up: "What percentage of total DCF value does terminal value typically represent according to the sources, and what is the typical or recommended length of the high-growth (explicit forecast) period in years?"

## คำตอบสรุป

- Gordon growth (going concern แบบ perpetuity): TV ณ ปี n = CF ของปี n+1 หาร (r − g) โดย r คือ cost of equity (สำหรับ equity/dividend) หรือ cost of capital (สำหรับ firm) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- Exit multiple (pricing): TV = ตัวชี้วัดปีสุดท้าย x multiple ที่ประมาณไว้ และ source ระบุว่าวิธีนี้ "Never appropriate in an intrinsic valuation" — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ใน bank valuation exit multiple ที่ใช้บ่อยคือ P/BV และ justified P/BV = (ROE − g) / (ke − g) ซึ่งมาจาก Gordon growth model — [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- Cap ของ stable growth: ต้องไม่เกินอัตราเติบโตของเศรษฐกิจ แต่ต่ำกว่าได้ และติดลบได้สำหรับธุรกิจขาลง — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ถ้าใช้ cash flow และ discount rate แบบ nominal ต้องใช้ g แบบ nominal ในสกุลเงินเดียวกัน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ที่มาของ cap เทียบกับ risk-free: risk-free = expected inflation + real interest rate, nominal GDP growth = expected inflation + real growth ในระยะยาว real growth ไม่ควรต่ำกว่า real interest rate จึงใช้ risk-free เป็นเพดานโดยปริยาย — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ถ้าตั้ง nominal growth ของเศรษฐกิจสูงแต่ risk-free ต่ำ จะ overvalue และกลับกันจะ undervalue — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ตัวอย่างใน source: Excess Return Model ของ Bank of America ใช้ terminal growth 3% ตาม GDP growth ของประเทศ เพราะบริษัทโตเกินนั้นไม่ได้ — [How to: Excess Return Model for Valuing Financial Stocks]
- ความสัมพันธ์ของ growth, reinvestment, ROIC: g = reinvestment rate x ROC (ส่วนฝั่ง equity คือ g = retention x ROE) ดังนั้นใน stable growth reinvestment rate = g / ROC และ payout ratio = 1 − g / ROE — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- สูตร TV แบบ fundamental: แทน reinvestment rate = g/ROC ลงใน FCFF ปีหน้า (EBIT(1−t) x (1 − g/ROC)) แล้วหารด้วย (WACC − g) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ใน stable growth excess returns ควรเข้าใกล้ศูนย์ (ROC เข้าหา cost of capital, ROE เข้าหา cost of equity) beta เข้าใกล้ 1 และ debt ratio เข้าใกล้ค่าเฉลี่ยอุตสาหกรรม แต่ source ก็ยอมรับว่า McKinsey ให้ ROC = cost of capital เสมอ ส่วน Damodaran เห็นว่า excess return อาจอยู่นานมาก — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- สัดส่วน TV ต่อมูลค่ารวม: source ไม่ได้ระบุกฎตายตัว มีเพียงตัวอย่าง Heineken ที่ PV ของ TV ราว 36.4 พันล้านยูโรจาก operating assets ราว 51.7 พันล้านยูโร (ประมาณ 70%) และ Luminor Bank (residual income model) ที่ TV คิดเป็น 46% ของมูลค่ารวม (อีก 43% มาจาก book equity และ 11% จาก residual income ช่วง forecast) — [Aswath Damodaran Updated: January 2026 - NYU Stern], [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK ... LUMINOR - Digikogu]
- ความยาว explicit forecast: source ไม่ให้ตัวเลขตายตัว ตัวอย่างที่พบคือ 10 ปีในกรณี Heineken และ 5 ปีในกรณี Luminor (2025–2029) และ Damodaran ระบุว่าปัจจัยที่กำหนดความยาวคือขนาดธุรกิจเทียบกับตลาด ความแข็งแรงของ competitive advantage การแข่งขัน และกฎระเบียบ ยิ่งตลาดใหญ่ ธุรกิจเล็กเทียบตลาด และ moat แข็ง ยิ่งโตได้นาน — [Aswath Damodaran Updated: January 2026 - NYU Stern], [ESTIMATING THE VALUE OF A PRIVATELY HELD BANK ... LUMINOR - Digikogu], [Valuing Financial Service Firms (Damodaran, Investment Valuation 3rd ed. Ch.21) - NYU Stern]

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Never appropriate in an intrinsic valuation." |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "The stable growth rate cannot exceed the growth rate of the economy" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Reinvestment Rate = Stable g/ Stable period ROC = g/ ROC" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Stable period payout ratio = 1 - g/ ROE" |
| How to: Excess Return Model for Valuing Financial Stocks | "the company CANNOT grow beyond that rate into the future" |
| ESTIMATING THE VALUE OF A PRIVATELY HELD BANK ... - Digikogu | "43% from equity, 11% from forecasted residual income (RI), and 46% from terminal value" |

## สิ่งที่ไม่พบใน notebook

- ไม่พบกฎทั่วไปว่า TV ควรเป็นสัดส่วนเท่าไรของมูลค่ารวม มีเพียงตัวอย่างรายบริษัท (Heineken ประมาณ 70%, Luminor 46%) คำตอบแรกของ notebook พูดว่า "50% ถึง 80%+" แต่ citation รองรับเฉพาะสองตัวอย่างนี้ จึงไม่นำมาใช้เป็นกฎ ส่วนตัวเลข Amazon และ Bed Bath & Beyond ที่ follow-up ให้มาไม่มีข้อความอ้างอิงยืนยัน จึงตัดทิ้ง
- ไม่พบกฎทั่วไปว่า explicit forecast ควรกี่ปี มีเพียงตัวอย่างและปัจจัยกำหนด ข้อความ "5 ถึง 10 ปี" ของ notebook ไม่มี citation ที่ระบุตรง ๆ
- ตัวเลข cap ที่ชัดเจน (เช่น ไม่เกิน risk-free กี่จุด) ไม่มี มี เพียงหลักการว่า risk-free เป็นเพดานโดยปริยาย
