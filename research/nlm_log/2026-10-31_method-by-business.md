# แผนที่วิธี valuation ตามประเภทธุรกิจ และการจัดการ lease (IFRS 16)

- **วันที่ถาม:** 2026-10-31
- **notebook:** Valuation Methods (alias `valuation-methods`)
- **conversation_id:** 60d6c66c-76eb-4260-a4df-057bbd219f4a (คำถามหลัก), 82cca826-5fc6-41a4-afa6-9a46f0ba9a04 (คำถามติดตาม 1 ข้อ เพื่อตรวจ lease/IFRS 16 และ emerging market)

## คำถาม

คำถามหลัก: Give a mapping of business type to preferred and avoided valuation methods for: mature stable firms, high-growth firms, emerging market firms, retailers and consumer firms with heavy leases, financials, REITs, and cyclicals. Also explain how lease commitments (IFRS 16) should be treated in DCF and in EV/EBITDA.

คำถามติดตาม: Using only what the sources explicitly state: (A) How should IFRS 16 / capitalised operating leases be handled in FCFF DCF (EBIT, WACC weights, bridge from EV to equity) and in EV/EBITDA (EV numerator and EBITDA denominator consistency, EBITDAR)? (B) For emerging market firms, what do the sources say about country risk premium, valuing in real vs nominal terms under high inflation, and which valuation method or multiples are preferred or avoided? State clearly if a point is not covered in the sources.

## คำตอบสรุป

**Mature / stable firms**

- เหมาะ: DDM เมื่อปันผล (รวม buyback) ใกล้เคียง FCFE, stable growth model หรือ 2-stage ถ้าบริษัทใหญ่และโตใกล้เศรษฐกิจ, relative multiples — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Business Analysis and Valuation - docenti.unina.it]
- เลี่ยง: โมเดล 3-stage/n-stage ที่ซับซ้อนเกินจำเป็น และ liquidation value (ใช้เมื่อบริษัทกำลังเลิกกิจการ) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- กติกาเลือกโมเดลของ Damodaran: ใช้ FCFE model แทน DDM ถ้าปันผลต่ำกว่า 80% หรือสูงกว่า 110% ของ FCFE ในช่วง 5 ปี — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- อัตราเติบโตระยะยาวต้องไม่เกินอัตราเติบโตของเศรษฐกิจ — [Aswath Damodaran Updated: January 2026 - NYU Stern]

**High-growth firms**

- เหมาะ: โมเดล 3-stage หรือ n-stage (บริษัทเล็กโตเร็วมาก คือเกินอัตราเติบโตเศรษฐกิจ + 10% หรือมีกำแพงการเข้าสู่ธุรกิจสูง) และ real options สำหรับสินทรัพย์ที่เป็นสิทธิ์ เช่น สิทธิบัตรหรือ pipeline — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern] (ส่วน options ของแหล่งสำรอง)
- เลี่ยง: stable growth ที่ตั้งอัตราเติบโตสูงกว่าเศรษฐกิจ และ multiples จากกำไรย้อนหลัง (กำไรปัจจุบันถูกกดโดยค่าใช้จ่ายขยายธุรกิจ/R&D) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- กระแสเงินสดช่วงแรกติดลบได้และบริษัทยังมีมูลค่าถ้ากระแสเงินสดช่วงหลังมากพอ — [Aswath Damodaran Updated: January 2026 - NYU Stern]

**Emerging market firms**

- ต้องสะท้อน country risk ด้วย country risk premium (CRP) ได้จาก default spread ของพันธบัตรรัฐบาล, CDS, rating, หรือปรับตามความผันผวนสัมพัทธ์ของตลาดหุ้น และจะใส่ CRP ในรูปแบบคงที่ หรือถ่วงตามที่มาของรายได้ (แนวคิด lambda) — [Aswath Damodaran Updated: January 2026 - NYU Stern], [Equity Risk Premiums: Globalization and Country risk - Musings on Markets]
- งานวิจัยใน BRIC ที่ notebook อ้างว่า CRP แบบปรับด้วยความผันผวนอธิบายผลตอบแทนได้ดีกว่า raw yield spread โดยเฉพาะจีนและอินเดีย — [Valuation in High Growth Markets - DiVA-Portal]
- ถ้าเงินเฟ้อสูง (>10%) ให้เปลี่ยนไปใช้ real cash flows กับ real discount rate กระแสเงินสดและอัตราคิดลดต้องสอดคล้องกันเรื่องสกุลเงินและเงินเฟ้อ — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- เลี่ยง: CAPM ที่ใช้ beta ท้องถิ่นโดยไม่ปรับ เพราะ beta ตลาดเกิดใหม่มักต่ำเกินจริง (ตลาดแยกส่วนและขาดสภาพคล่อง) — [Valuation in High Growth Markets - DiVA-Portal]
- ตลาดเกิดใหม่ประเมินยากเพราะโครงสร้างบริษัท ความเสี่ยงประเทศ และธรรมาภิบาล — [Aswath Damodaran Updated: January 2026 - NYU Stern]

**Retailers / consumer firms ที่เช่าพื้นที่มาก**

- ค่าเช่าดำเนินงาน (operating lease) เป็นภาระผูกพันตามสัญญา ควรปฏิบัติเป็นค่าใช้จ่ายทางการเงิน: debt value ของ lease = PV ของ lease commitments คิดลดที่ต้นทุนหนี้ก่อนภาษี และสร้าง lease asset มูลค่าเท่ากัน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ปรับ operating income: Adjusted EBIT = stated EBIT + ค่าเช่าปีนี้ - ค่าเสื่อมของ lease asset (ประมาณได้เป็น stated EBIT + ต้นทุนหนี้ก่อนภาษี x PV ของ lease) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- ตัวอย่างของ The Gap ใน source: debt value ของ lease ราว 4,397 ล้านดอลลาร์ รวมหนี้เป็น 6,367 ล้านดอลลาร์ ปรับ operating income จาก 1,012 เป็น 1,362 ล้านดอลลาร์ cost of capital ลดจาก 7.31% เป็น 6.25% และ return on capital ลดจาก 12.90% เป็น 9.30% (เป็นตัวอย่างของ source ไม่ใช่ตัวเลขอ้างอิงของหุ้นอื่น) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- source ระบุว่าตั้งแต่ปี 2019 ทั้ง IFRS และ GAAP กำหนดให้บริษัทบันทึก lease เป็นหนี้และสินทรัพย์ในงบดุล — [Aswath Damodaran Updated: January 2026 - NYU Stern]

**การจัดการ lease ใน DCF (FCFF)**

- EBIT: ปรับตามสูตรข้างบน ส่วนดอกเบี้ยจะเพิ่มและ net income ไม่ควรเปลี่ยน — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- WACC: หนี้รวมสำหรับถ่วงน้ำหนักต้องรวม lease debt (ตัวอย่าง Gap) — [Aswath Damodaran Updated: January 2026 - NYU Stern]
- สะพานจาก enterprise value ไป equity value: ต้องหัก lease debt เช่นเดียวกับหนี้ปกติ — [Aswath Damodaran Updated: January 2026 - NYU Stern]

**Financials, REITs, Cyclicals** (รายละเอียดอยู่ใน log แยก)

- Financials: เหมาะ DDM, FCFE (regulatory capital), excess return/RIM, P/BV, P/tBV, P/E เลี่ยง FCFF/WACC/EV multiples เพราะหนี้คือวัตถุดิบ และ capex/working capital นิยามไม่ได้ — [Valuing Financial Service Firms (Damodaran paper, 2009)], [Estimating the Value of a Privately Held Bank: Luminor Bank AS], [A Case Study of Bank Equity Valuation Methods ... - MDPI]
- REITs: เหมาะ NAV (หรือ UAV), P/AFFO, DCF บน AFFO เลี่ยง GAAP net income / P/E — [REIT Valuation Methods - Financial Edge Training], [REIT Valuation The NAV-based Pricing Model - Green Street]
- Cyclicals/commodity: เหมาะ normalized DCF และ multiples บนกำไร normalized, real options สำหรับแหล่งสำรองที่ยังไม่พัฒนา เลี่ยง base-year DCF และ P/E หรือ EV/EBITDA ปีเดียวที่จุดสูงสุดหรือต่ำสุด — [Ups and Downs: Valuing Cyclical and Commodity Companies - NYU Stern]

**ตารางสรุป**

| ประเภทธุรกิจ | เหมาะ | เลี่ยง |
|---|---|---|
| Mature / stable | DDM, stable หรือ 2-stage DCF, multiples | 3-stage ที่ซับซ้อนเกิน, liquidation value |
| High-growth | 3-stage / n-stage DCF, real options | stable growth, trailing earnings multiples |
| Emerging market | DCF + CRP, real cash flow เมื่อเงินเฟ้อ >10% | CAPM ท้องถิ่นไม่ปรับ, nominal DCF ใต้เงินเฟ้อสูง |
| Retail / heavy lease | FCFF และ multiples ที่ capitalize lease แล้ว | EBIT/หนี้ที่ไม่ปรับ lease |
| Financials | DDM, FCFE, RIM, P/BV, P/tBV | FCFF, WACC, EV/EBITDA |
| REITs | NAV/UAV, P/AFFO, DCF บน AFFO | GAAP EPS / P/E |
| Cyclical / commodity | normalized DCF และ multiples | base-year DCF, peak/trough multiples |

## หลักฐานจาก source

| source | ข้อความสั้น (≤15 คำ) |
|---|---|
| Aswath Damodaran Updated: January 2026 - NYU Stern | "If inflation is high (>10%) switch to real cash flows" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "operating lease expenses should be treated as financing expenses" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Debt Value of Operating Leases = Present value of Operating Lease Commitments" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "In 2019, both IFRS and GAAP made a major shift on operating leases" |
| Aswath Damodaran Updated: January 2026 - NYU Stern | "Use a 3-Stage or n-stage Model" |
| Valuing Financial Service Firms (Damodaran paper, 2009) - NYU Stern | "best valued using equity valuation models, rather than enterprise valuation models" |

## สิ่งที่ไม่พบใน notebook

- **EV/EBITDA กับ IFRS 16 ไม่พบใน notebook:** คำถามติดตามที่ถามเจาะจง notebook ตอบชัดว่า source ไม่ได้พูดถึง EBITDAR หรือกฎความสอดคล้องระหว่าง EV (ตัวตั้ง) กับ EBITDA (ตัวหาร) ภายใต้ IFRS 16 ในคำตอบหลักมีข้อความว่า "EBITDA ภายใต้ IFRS 16 เท่ากับ EBITDAR ก่อน IFRS 16 และต้องจับคู่กับ EV ที่รวม lease debt" แต่เมื่อตรวจ cited_text แล้วไม่มี source ไหนยืนยัน จึงตัดทิ้งและไม่ควรนำไปใช้อ้างอิง (ควรหา source เพิ่ม หรือระบุว่าเป็นหลักการทั่วไปที่ผู้เรียนอธิบายเอง)
- **ข้ออ้าง "การรวม lease debt ทำให้ WACC ต่ำลงเสมอ":** ในคำตอบหลักเป็นข้อสรุปทั่วไปของ notebook แต่ source ยืนยันเฉพาะตัวอย่าง The Gap (7.31% เป็น 6.25%) จึงอย่าสรุปเกินตัวอย่างนั้น
- ตัวเลือกวิธีสำหรับ emerging market ที่ notebook ตอบมักอิงข้อมูลเรื่องธนาคาร (RIM, WEM) จาก source ธนาคารในแอฟริกา ไม่ใช่กฎทั่วไปของบริษัทตลาดเกิดใหม่ทุกประเภท
- ไม่มีตัวเลข CRP รายประเทศ (เช่น ไทย) ใน notebook ที่ตรวจได้ และ source ปี 2012 (Musings on Markets) เก่า ต้องดึงค่าล่าสุดจาก Trust sources ใน spec.md
- ไม่มีแนวทางเฉพาะสำหรับบริษัทที่ใช้ IFRS 16 ในประเทศไทย
